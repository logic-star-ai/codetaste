"""Run inference on benchmark instances using agent scripts."""
import asyncio
import csv
import os
import sys

import docker

from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow


# --- Configuration ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
MAX_CONCURRENT_INSTANCES = 3

# Initialize logging
setup_logging(LOG_DIR)
inference_logger = get_logger("inference")

# --- Docker/Podman Client Setup ---
try:
    client: docker.DockerClient = docker.from_env(timeout=300)
    client.ping()
except Exception as e:
    inference_logger.error(f"Docker/Podman connection failed: {e}")
    inference_logger.error("Hint: export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock")
    sys.exit(1)


def execute_instance(instance_row: InstanceRow, force: bool = False) -> bool:
    """
    Execute inference on a benchmark instance.

    Args:
        instance_row: The benchmark instance to run inference on
        force: If True, run inference even if prediction.diff already exists

    Returns:
        True if successful, False otherwise
    """
    # Create instance-specific logger
    instance_logger = get_logger(
        f"{instance_row.id}__inference",
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
        return False

    try:
        # Run container in inference mode (detached to stream logs)
        instance_logger.info("Running container in inference mode...")
        container = client.containers.run(
            instance_row.runtime_image,
            command="inference",
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY},
            volumes={
                agent_dir: {"bind": "/agent", "mode": "rw"},
                instance_output_dir: {"bind": "/output", "mode": "rw"},
            },
            working_dir="/testbed",
        )

        # Stream container output to log
        try:
            for log_line in container.logs(stream=True, follow=True):
                instance_logger.info(log_line.decode('utf-8', errors='replace').rstrip())
        except Exception as log_error:
            instance_logger.warning(f"Error streaming logs: {log_error}")

        # Wait for container to finish and get exit code
        result = container.wait()
        exit_code = result.get('StatusCode', -1)

        # Remove container
        try:
            container.remove(force=True)
        except Exception:
            pass  # Container might already be removed

        if exit_code == 0:
            inference_logger.info(f"[{instance_row.id}]: ✅ Inference completed successfully")
            instance_logger.info("✅ Inference completed successfully")
            return True
        else:
            inference_logger.error(f"[{instance_row.id}]: ❌ Container exited with code {exit_code}")
            instance_logger.error(f"❌ Container exited with code {exit_code}")
            return False

    except docker.errors.ContainerError as e:
        inference_logger.error(f"[{instance_row.id}]: ❌ Container error (exit code {e.exit_status})")
        instance_logger.error(f"❌ Container error (exit code {e.exit_status})")
        if e.stderr:
            instance_logger.error(f"Error output: {e.stderr.decode()}")
        return False
    except docker.errors.ImageNotFound:
        inference_logger.error(f"[{instance_row.id}]: ❌ Runtime image not found: {instance_row.runtime_image}")
        instance_logger.error(f"❌ Runtime image not found: {instance_row.runtime_image}")
        instance_logger.error("Run bootstrap first to create the image")
        return False
    except docker.errors.APIError as e:
        inference_logger.error(f"[{instance_row.id}]: ❌ Docker API error: {e}")
        instance_logger.error(f"❌ Docker API error: {e}")
        return False
    except Exception as e:
        inference_logger.exception(f"[{instance_row.id}]: ❌ Unexpected error: {e}")
        instance_logger.exception(f"❌ Unexpected error: {e}")
        return False


async def inference_parallel(instances: list[InstanceRow], degree: int):
    """
    Orchestrates parallel inference execution using a semaphore.

    Args:
        instances: List of instances to run inference on
        degree: Maximum number of concurrent instances
    """
    semaphore = asyncio.Semaphore(degree)

    async def sem_task(instance: InstanceRow):
        async with semaphore:
            try:
                return await asyncio.wait_for(
                    asyncio.to_thread(execute_instance, instance),
                    timeout=3600  # 1 hour timeout per instance
                )
            except asyncio.TimeoutError:
                inference_logger.error(f"⚠️ Inference timed out (60 min) for {instance.id}")
                return False

    tasks = [sem_task(inst) for inst in instances]
    await asyncio.gather(*tasks)


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

    instances_to_run = instances[:8]
    inference_logger.info(f"Running inference on {len(instances_to_run)} instances (max {MAX_CONCURRENT_INSTANCES} concurrent)")

    # Run instances in parallel
    asyncio.run(inference_parallel(instances_to_run, MAX_CONCURRENT_INSTANCES))


if __name__ == "__main__":
    main()
