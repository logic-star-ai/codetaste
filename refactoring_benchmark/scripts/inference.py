"""Run inference on benchmark instances using agent scripts."""
import atexit
import csv
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow
from refactoring_benchmark.utils.container_utils import (
    stop_and_remove_container,
    register_container,
    cleanup_all_containers,
    get_local_client,
    safe_container_run,
)


# --- Configuration ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
NR_PARALLEL_PROCESSES = 10
TIMEOUT_INFERENCE = 3600  # 1 hour per instance

# Initialize logging
setup_logging(LOG_DIR)
inference_logger = get_logger("inference")


def execute_instance(instance_row: InstanceRow, force: bool = False) -> bool:
    """
    Execute inference on a benchmark instance.

    Args:
        instance_row: The benchmark instance to run inference on
        force: If True, run inference even if prediction.diff already exists

    Returns:
        True if successful, False otherwise
    """
    # Get process-local Podman client
    client = get_local_client()
    if not client:
        return False

    # Create instance-specific logger
    instance_logger = get_logger(
        f"inference-{instance_row.id}",
        use_file=True,
        use_stdout=False
    )

    instance_output_dir = os.path.abspath(
        os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    )
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if os.path.exists(prediction_diff) and not force:
        inference_logger.info(f"[{instance_row.id}]: Skipping inference, prediction.diff already exists")
        instance_logger.info("Skipping inference, prediction.diff already exists")
        client.close()
        return True

    agent_dir = os.path.abspath(os.path.join(PROJECT_ROOT, "agent"))
    os.makedirs(instance_output_dir, exist_ok=True)

    inference_logger.info(f"[{instance_row.id}]: Starting inference")
    instance_logger.info(f"Starting inference for {instance_row.display_path}")
    instance_logger.info(f"  Image: {instance_row.runtime_image}")
    instance_logger.info(f"  Output: {instance_output_dir}")

    # Validate paths
    if not os.path.exists(agent_dir):
        inference_logger.error(f"[{instance_row.id}]: Agent directory not found: {agent_dir}")
        instance_logger.error(f"Agent directory not found: {agent_dir}")
        client.close()
        return False

    container: Optional[PodmanContainer] = None

    try:
        # Verify image exists
        try:
            client.images.get(instance_row.runtime_image)
        except podman.errors.ImageNotFound:
            inference_logger.error(f"[{instance_row.id}]: ❌ Runtime image not found: {instance_row.runtime_image}")
            instance_logger.error(f"❌ Runtime image not found: {instance_row.runtime_image}")
            instance_logger.error("Run bootstrap first to create the image")
            return False

        # Run container in inference mode
        instance_logger.info("Running container in inference mode...")
        container = safe_container_run(
            client,
            instance_row.runtime_image,
            command=["inference"],
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY or ""},
            volumes={
                agent_dir: {"bind": "/agent", "mode": "rw"},
                instance_output_dir: {"bind": "/output", "mode": "rw"},
            },
            working_dir="/testbed",
        )
        register_container(container)

        # Stream container output to log
        try:
            for log_line in container.logs(stream=True, follow=True):
                instance_logger.info(log_line.decode('utf-8', errors='replace').rstrip())
        except Exception as log_error:
            instance_logger.warning(f"Error streaming logs: {log_error}")

        # Wait for container to finish and get exit code
        exit_code = container.wait()


        if exit_code == 0:
            inference_logger.info(f"[{instance_row.id}]: ✅ Inference completed successfully")
            instance_logger.info("✅ Inference completed successfully")
            return True
        else:
            inference_logger.error(f"[{instance_row.id}]: ❌ Container exited with code {exit_code}")
            instance_logger.error(f"❌ Container exited with code {exit_code}")
            return False

    finally:
        if container is not None:
            stop_and_remove_container(container)
        client.close()


def execute_instance_wrapper(instance: InstanceRow):
    """Wrapper for execute_instance for use with ProcessPoolExecutor."""
    try:
        return execute_instance(instance)
    except Exception as e:
        inference_logger.error(f"[{instance.id}]: ❌ FAILED with exception: {e}")
        return False


def inference_parallel(instances: list[InstanceRow]):
    """
    Orchestrates parallel inference execution using ProcessPoolExecutor.

    Args:
        instances: List of instances to run inference on
    """
    with ProcessPoolExecutor(NR_PARALLEL_PROCESSES) as executor:
        future_to_instance = {executor.submit(execute_instance_wrapper, inst): inst for inst in instances}
        all_futures_remaining = set(future_to_instance.keys())

        inference_logger.info(f"🚀 Running inference on {len(instances)} instances with up to {NR_PARALLEL_PROCESSES} parallel processes...")
        inference_logger.info(f"Remaining instances {len(all_futures_remaining)}: {[future_to_instance[future].id for future in list(all_futures_remaining)[:3]]} ...")

        for future in as_completed(future_to_instance):
            instance = future_to_instance[future]
            try:
                success = future.result(timeout=TIMEOUT_INFERENCE + 60)
                all_futures_remaining.remove(future)
                status = "✅" if success else "❌"
                inference_logger.info(f"{status} [{instance.id}] completed")
                inference_logger.info(f"Remaining instances {len(all_futures_remaining)}: {[future_to_instance[f].id for f in list(all_futures_remaining)[:3]]} ...")
            except Exception as e:
                inference_logger.error(f"[{instance.id}]: Unexpected orchestration error: {e}")
                all_futures_remaining.discard(future)


def main():
    """Main entry point for the inference script."""
    if not API_KEY:
        inference_logger.error("Missing ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Load instances from CSV
    instances = []
    try:
        with open(CSV_FILE, "r") as f:
            for row in csv.DictReader(f):
                instances.append(InstanceRow(**row))
    except FileNotFoundError:
        inference_logger.error(f"Instances file not found: {CSV_FILE}")
        sys.exit(1)
    except Exception as e:
        inference_logger.error(f"Failed to load instances: {e}")
        sys.exit(1)

    if not instances:
        inference_logger.warning("No instances found in CSV")
        return

    inference_logger.info(f"Loaded {len(instances)} instances")

    # Run subset of instances (adjust as needed)
    instances_to_run = instances[:5]

    if instances_to_run:
        inference_parallel(instances_to_run)


if __name__ == "__main__":
    def signal_handler(signum, _frame):
        inference_logger.warning(f"\n⚠️ Received {signal.Signals(signum).name}. Terminating and cleaning...")
        cleanup_all_containers()
        time.sleep(30)
        os._exit(1)

    atexit.register(cleanup_all_containers)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
