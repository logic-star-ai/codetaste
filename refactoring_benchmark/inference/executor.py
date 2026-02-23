"""Executor for running inference on benchmark instances."""

import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from tqdm import tqdm

from refactoring_benchmark.inference.models import InferenceConfig
from refactoring_benchmark.inference.runner import InstanceInferenceRunner
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow


def run_single_instance(instance: InstanceRow, config: InferenceConfig) -> bool:
    """
    Run inference on a single benchmark instance.

    This is a wrapper around InstanceInferenceRunner for backward compatibility.

    Args:
        instance: Instance row from CSV
        config: Inference configuration

    Returns:
        True if inference completed successfully, False otherwise
    """
    runner = InstanceInferenceRunner(instance, config)
    return runner.run()


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
