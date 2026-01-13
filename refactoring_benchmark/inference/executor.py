"""Executor for running inference on benchmark instances."""

import os
import shutil
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional

import podman
from podman.domain.containers import Container as PodmanContainer
from tqdm import tqdm

from refactoring_benchmark.inference.models import InferenceConfig
from refactoring_benchmark.inference.utils import (
    augment_inference_metadata_with_description_type,
    copy_agent_config,
    create_fallback_inference_metadata,
    ensure_inference_metadata_exists,
    get_instance_output_dir,
    output_exists,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow


def run_single_instance(instance: InstanceRow, config: InferenceConfig) -> bool:
    """
    Run inference on a single benchmark instance.

    Args:
        instance: The benchmark instance to run inference on
        config: Inference configuration

    Returns:
        True if successful, False otherwise
    """
    instance_logger = get_logger(
        f"{instance.id}", use_file=True, use_stdout=False, log_subdir=f"{config.sanitized_agent_id}"
    )
    output_dir = get_instance_output_dir(instance, config.sanitized_agent_id, config.output_dir)

    # Check if output already exists (skip unless force)
    if output_exists(output_dir) and not config.force:
        instance_logger.info(f"Skipping {instance.id}, output already exists at {output_dir}")
        return True

    # Create output directory
    if output_dir.exists() and output_dir.is_dir():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    

    # Copy metadata files
    try:
        copy_agent_config(config.agent_dir, output_dir)
    except FileNotFoundError as e:
        instance_logger.error(f"Failed to copy metadata: {e}")
        return False

    container: Optional[PodmanContainer] = None
    client = podman_utils.get_local_client()

    if not client:
        instance_logger.error("Failed to connect to Podman daemon")
        return False

    try:
        # Verify runtime image exists
        try:
            client.images.get(instance.runtime_image)
        except podman.errors.ImageNotFound:
            instance_logger.error(f"Runtime image not found: {instance.runtime_image}")
            instance_logger.error("Run bootstrap first to create the image")
            return False

        # Start inference
        instance_logger.info(f"Starting inference for {instance.display_path}")
        instance_logger.info(f"  Image: {instance.runtime_image}")
        instance_logger.info(f"  Output: {output_dir}")

        # Build environment variables for container
        container_env = {}
        container_env.update(config.env_vars)
        container_env["DESCRIPTION_TYPE"] = config.description_type

        # Run container in inference mode
        instance_logger.info("Running container in inference mode...")
        if container_env:
            instance_logger.info(f"  Environment variables: {', '.join(container_env.keys())}")
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["inference"],
            detach=True,
            environment=container_env,
            volumes={
                str(config.agent_dir): {"bind": "/agent", "mode": "rw"},
                str(output_dir): {"bind": "/output", "mode": "rw"},
            },
            working_dir="/testbed",
            remove=False,
            nano_cpus=int(8e9)
        )

        # Wait for container to finish with timeout
        try:
            exit_code = container.wait(timeout=config.timeout)
        except Exception as timeout_error:
            instance_logger.error(f"Container execution timed out after {config.timeout}s: {timeout_error}")
            # Create fallback metadata for timeout
            create_fallback_inference_metadata(output_dir, finish_reason="timeout", description_type=config.description_type)
            return False

        # container output to log
        raw_logs = container.logs(stream=False, follow=False)
        raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
        stdout = raw_logs.decode("utf-8", errors="replace")
        instance_logger.info(stdout)
        (output_dir / "inference.out").write_text(stdout, encoding="utf-8")

        # Check exit code
        prediction_path = output_dir / "prediction.diff"
        if exit_code == 0 and prediction_path.exists():
            instance_logger.info("Inference completed successfully")
            ensure_inference_metadata_exists(output_dir, description_type=config.description_type)
            augment_inference_metadata_with_description_type(output_dir, config.description_type)
            return True
        else:
            instance_logger.error(f"Container exited with code {exit_code}")
            # Check if prediction.diff exists to determine fallback reason
            if prediction_path.exists():
                # Agent produced output but failed
                ensure_inference_metadata_exists(output_dir, description_type=config.description_type)
                augment_inference_metadata_with_description_type(output_dir, config.description_type)
            else:
                # Agent crashed without producing output
                create_fallback_inference_metadata(output_dir, finish_reason="crashed", description_type=config.description_type)
            return False

    except Exception as e:
        instance_logger.error(f"Unexpected error during inference: {e}")
        # Create fallback metadata for crash
        create_fallback_inference_metadata(output_dir, finish_reason="crashed", additional={"error": str(e)}, description_type=config.description_type)
        return False

    finally:
        if container is not None:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                instance_logger.error(f"Failed to remove container [{instance.id}]: {e}")
        client.close()


class InferenceOrchestrator:
    """Orchestrates parallel inference execution with signal handling."""

    def __init__(self, instances: List[InstanceRow], config: InferenceConfig):
        """
        Initialize orchestrator.

        Args:
            instances: List of instances to run inference on
            config: Inference configuration
        """
        self.instances = instances
        self.config = config
        self.logger = get_logger("inference")
        self.executor = None

        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            sig_name = signal.Signals(signum).name
            self.logger.warning(f"\nReceived {sig_name}, initiating shutdown...")
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            self._cleanup_containers()
            print(f"Exiting due to {sig_name}")
            sys.exit()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _cleanup_containers(self):
        """Clean up all active containers."""
        self.logger.info("Cleaning up active containers...")
        podman_utils.cleanup_all_containers()

    def run(self) -> None:
        """
        Execute inference on all instances using ThreadPoolExecutor.

        Uses tqdm progress bar to track execution progress.
        """
        if not self.instances:
            self.logger.warning("No instances to run inference on")
            return

        self.logger.info(f"Starting inference on {len(self.instances)} instances")
        self.logger.info(f"Using {self.config.nr_workers} parallel workers")
        self.logger.info(f"Timeout per instance: {self.config.timeout}s")
        self.logger.info(f"Output directory: {self.config.output_dir}")

        results = {"success": 0, "failed": 0}
        interrupted = False

        # Don't use context manager - we want manual control over shutdown
        executor = ThreadPoolExecutor(max_workers=self.config.nr_workers)
        self.executor = executor

        try:
            # Submit all tasks
            future_to_instance = {
                executor.submit(run_single_instance, inst, self.config): inst for inst in self.instances
            }

            # Process completed tasks with progress bar
            with tqdm(total=len(self.instances), desc="Inference Progress", unit="instance") as pbar:
                for future in as_completed(future_to_instance):
                    instance = future_to_instance[future]

                    try:
                        success = future.result()
                        if success:
                            results["success"] += 1
                            status = "✅"
                        else:
                            results["failed"] += 1
                            status = "❌"

                        self.logger.info(f"{status} [{instance.id}] completed")

                    except Exception as e:
                        results["failed"] += 1
                        self.logger.error(f"❌ [{instance.id}] exception: {e}")

                    pbar.update(1)

        finally:
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            self._cleanup_containers()

            # Print summary
            total = results["success"] + results["failed"]
            self.logger.info("\n" + "=" * 50)
            self.logger.info("Inference Summary:")
            self.logger.info(f"  Total: {total}")
            self.logger.info(f"  Success: {results['success']}")
            self.logger.info(f"  Failed: {results['failed']}")
            self.logger.info("=" * 50)
