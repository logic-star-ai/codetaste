"""Executor for running inference on benchmark instances."""

import logging
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

from refactoring_benchmark.inference.models import InferenceConfig, InferenceMetadata
from refactoring_benchmark.inference.utils import (
    copy_agent_config,
    create_fallback_inference_metadata,
    get_instance_output_dir,
    output_exists,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow

def _output_container_logs(container: PodmanContainer, output_path: Path, instance_logger: logging.Logger) -> None:
    """Helper to output container logs to file and logger."""
    raw_logs = container.logs(stream=False, follow=False)
    raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
    stdout = raw_logs.decode("utf-8", errors="replace")
    instance_logger.error(stdout)
    output_path.write_text(stdout, encoding="utf-8")


def run_single_instance(instance: InstanceRow, config: InferenceConfig) -> bool:
    """Run inference on a single benchmark instance with streamlined checks."""
    instance_logger = get_logger(
        f"{instance.id}", use_file=True, use_stdout=False, log_subdir=f"{config.sanitized_agent_id}"
    )
    output_dir = get_instance_output_dir(instance, config.sanitized_agent_id, config.output_dir)

    # 1. Skip if already done
    if output_exists(output_dir) and not config.force:
        instance_logger.info(f"Skipping {instance.id}, output already exists.")
        try:
            metadata: InferenceMetadata = InferenceMetadata.load_from_json(output_dir / "inference_metadata.json")
            is_success = metadata.finish_reason.lower() == "success"
            if is_success or not config.force_unsuccessful:
                return is_success
        except Exception:
            return False

    # 2. Prepare environment
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    copy_agent_config(config.agent_dir, output_dir)

    client = podman_utils.get_local_client()
    if not client:
        instance_logger.error("Failed to connect to Podman")
        return False

    container: Optional[PodmanContainer] = None
    try:
        # 3. Execute Container
        instance_logger.info(f"Starting inference for {instance.display_path}")
        instance_logger.info(f"  Image: {instance.runtime_image}")
        instance_logger.info(f"  Output: {output_dir}")
        env = {**config.env_vars, "DESCRIPTION_TYPE": config.description_type}
        instance_logger.debug(f"  Environment Variables: {[(k, v[:10] if isinstance(v, str) else v) for k, v in env.items()]}")
        
        # The run_agent provided is responsible for catching errors and adjusting finish_reason in inference_metadata.json
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["inference"],
            detach=True,
            environment=env,
            volumes={
                str(config.agent_dir): {"bind": "/agent", "mode": "rw"},
                str(output_dir): {"bind": "/output", "mode": "rw"},
            },
            working_dir="/testbed",
            remove=False,
            nano_cpus=int(8e9)
        )

        try:
            container.wait(timeout=config.timeout)
        except Exception as e:
            instance_logger.error(f"Execution timed out: {e}")
            create_fallback_inference_metadata(
                output_dir, 
                "timeout", 
                config.description_type, 
                additional={"error": f"Container timed out: {str(e)}"}
                )
        
        _output_container_logs(container, output_dir / "inference.out", instance_logger)

        # 4. Validation
        metadata_path = output_dir / "inference_metadata.json"
        prediction_path = output_dir / "prediction.diff"

        # Check A: Metadata exists
        if not metadata_path.exists():
            instance_logger.error("Agent failed to create inference_metadata.json")
            return False

        # Check B: Prediction exists
        if not prediction_path.exists():
            instance_logger.error("Agent or entrypoint.sh failed to generate / create prediction.diff")
            return False

        # Check C: Success reason
        metadata = InferenceMetadata.load_from_json(metadata_path)
        is_success = metadata.finish_reason.lower() == "success"
        metadata.description_type = config.description_type
        metadata.save_to_json(metadata_path)
        
        if is_success:
            instance_logger.info("Inference completed successfully")
        else:
            instance_logger.error(f"Inference failed with reason: {metadata.finish_reason} {metadata.additional}")
            
        return is_success

    except Exception as e:
        instance_logger.error(f"Unexpected error: {e}")
        return False
    finally:
        if container:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                instance_logger.warning(f"Failed to remove container [{instance.id}]. Probably already removed. Error: {e}")
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
