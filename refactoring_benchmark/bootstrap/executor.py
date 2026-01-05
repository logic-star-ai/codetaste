"""Bootstrap orchestration with ThreadPool execution."""

import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional
from concurrent.futures import TimeoutError

from tqdm import tqdm

from refactoring_benchmark.bootstrap.models import BootstrapConfig
from refactoring_benchmark.bootstrap.setup import bootstrap_setup_phase
from refactoring_benchmark.bootstrap.runtime import bootstrap_runtime_phase
from refactoring_benchmark.bootstrap.utils import BootstrapError
from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow


def bootstrap_single_instance(instance: InstanceRow, config: BootstrapConfig) -> bool:
    """
    Bootstrap a single instance with retry logic.

    Args:
        instance: Benchmark instance
        config: Bootstrap configuration

    Returns:
        True if successful, False otherwise
    """
    instance_logger = get_logger(f"bootstrap-{instance.id}", use_file=True, use_stdout=False)
    instance_dir = instance.instance_dir()
    metadata_path = Path(instance_dir) / "instance_metadata.json"

    # Check if already bootstrapped
    if metadata_path.exists():
        metadata = ExecutionInstanceMetadata.load_from_json(metadata_path)
        client = podman_utils.get_local_client(80 * 60)
        if not podman_utils.is_image_existing(client, metadata.setup_image):
            instance_logger.error(f"Inconsistent state: Setup image missing for instance {instance.id} but metadata exists. Remove metadata to bootstrap setup again.")
            return False
        if config.force_runtime_build:
            instance_logger.info(
                f"⚠️  FORCING runtime phase for instance: {instance.id} with existing metadata."
            )
            try:
                bootstrap_runtime_phase(
                    client, instance, instance.setup_image, config, instance_logger, metadata=metadata, force=True
                )
                instance_logger.info(f"✅ Successfully rebuilt runtime for instance: {instance.id}")
                return True
            except Exception as e:
                instance_logger.error(f"Failed to rebuild runtime: {e}")
                return False
            finally:
                if client is not None:
                    client.close()
        else:
            instance_logger.info(f"⏭️  SKIPPING: Instance already bootstrapped: {instance.id}")
            return True

    # Initialize metadata
    metadata = ExecutionInstanceMetadata(
        owner=instance.owner,
        repo=instance.repo,
        base_hash=instance.commit_hash,
        golden_hash=instance.golden_commit_hash,
        setup_image=instance.setup_image,
        runtime_image=instance.runtime_image,
    )

    client = None
    try:
        # Check if language is supported
        is_supported = any(
            lang in instance.language.lower() for lang in config.supported_languages
        )
        client = podman_utils.get_local_client(120 * 60)

        # Attempt 1: Bootstrap with agent
        try:
            setup_img = bootstrap_setup_phase(
                client, instance, metadata, config, instance_logger, use_base_image=not is_supported
            )
            bootstrap_runtime_phase(client, instance, setup_img, config, instance_logger, metadata=metadata)
            instance_logger.info(f"✅ Successfully bootstrapped {instance.id}.")
        # Attempt 2: Fallback to base image
        except (RuntimeError, TimeoutError, BootstrapError) as e:
            instance_logger.error(
                f"Attempt 1 failed ({e}). Retrying with base image without execution environment..."
            )
            setup_img = bootstrap_setup_phase(
                client, instance, metadata, config, instance_logger, use_base_image=True
            )
            bootstrap_runtime_phase(client, instance, setup_img, config, instance_logger, metadata=metadata)
            instance_logger.info(f"✅ Successfully bootstrapped {instance.id} on retry with base image.")
        # Save metadata
        metadata.save_to_json(metadata_path)
        return True

    except Exception as e:
        instance_logger.error(f"❌ FAILED to bootstrap after retry: {e}")
        return False

    finally:
        if client is not None:
            client.close()


class BootstrapOrchestrator:
    """Orchestrates parallel bootstrap execution."""

    def __init__(self, instances: List[InstanceRow], config: BootstrapConfig):
        """
        Initialize orchestrator.

        Args:
            instances: List of instances to bootstrap
            config: Bootstrap configuration
        """
        self.instances = instances
        self.config = config
        self.logger = get_logger("bootstrap")
        self.executor = None

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            sig_name = signal.Signals(signum).name
            self.logger.warning(f"\nReceived {sig_name}, initiating shutdown...")
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self._cleanup_containers()
            print(f"Exiting due to {sig_name}")
            sys.exit(1)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _cleanup_containers(self):
        """Clean up all active containers."""
        self.logger.info("Cleaning up active containers...")
        podman_utils.cleanup_all_containers()

    def run(self) -> None:
        """
        Execute bootstrap on all instances using ThreadPoolExecutor.

        Uses tqdm progress bar to track execution progress.
        """
        if not self.instances:
            self.logger.warning("No instances to bootstrap")
            return

        self.logger.info(f"Starting bootstrap for {len(self.instances)} instances")
        self.logger.info(f"Using {self.config.nr_workers} parallel workers")

        results = {"success": 0, "failed": 0}

        # Manual executor management for proper shutdown control
        executor = ThreadPoolExecutor(max_workers=self.config.nr_workers)
        self.executor = executor

        try:
            # Submit all tasks
            future_to_instance = {
                executor.submit(bootstrap_single_instance, inst, self.config): inst
                for inst in self.instances
            }

            # Process completed tasks with progress bar
            with tqdm(total=len(self.instances), desc="Bootstrap Progress", unit="instance") as pbar:
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
            self.logger.info("Bootstrap Summary:")
            self.logger.info(f"  Total: {total}")
            self.logger.info(f"  Success: {results['success']}")
            self.logger.info(f"  Failed: {results['failed']}")
            self.logger.info("=" * 50)
