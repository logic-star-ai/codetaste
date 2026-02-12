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


def bootstrap_single_instance(instance: InstanceRow, config: BootstrapConfig, is_interrupted: List[bool]) -> bool:
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

    # Validate mutual exclusivity
    flags = [config.rerun_metrics, config.force_full_build, config.force_runtime_build]
    if sum(flags) > 1:
        instance_logger.error("Only one of --rerun-metrics, --force-full-build, --force-runtime-build allowed")
        return False

    # Load or create metadata
    if metadata_path.exists():
        metadata = ExecutionInstanceMetadata.load_from_json(metadata_path)

        # Early skip if nothing to do
        if sum(flags) == 0:
            instance_logger.info(f"⏭️  SKIPPING: Instance already bootstrapped: {instance.id}")
            return True
    else:
        # New instance - can't use runtime-only or rerun-metrics flags
        if config.force_runtime_build or config.rerun_metrics:
            instance_logger.error(f"Cannot use --force-runtime-build or --rerun-metrics without existing metadata")
            return False

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
        client = podman_utils.get_local_client(120 * 60)

        # Handle runtime-only rebuild (special case)
        if config.force_runtime_build:
            # Validate setup image exists
            if not podman_utils.is_image_existing(client, metadata.setup_image):
                instance_logger.error(f"Setup image missing: {metadata.setup_image}")
                return False

            # Just rebuild runtime, reuse existing metadata
            bootstrap_runtime_phase(
                client, instance, instance.setup_image, config, instance_logger, metadata=metadata, force=True
            )
            instance_logger.info(f"✅ Successfully rebuilt runtime for: {instance.id}")
            return True

        # Run setup + runtime (with fallback for new/rebuild)
        is_supported = any(lang in instance.language.lower() for lang in config.supported_languages)
        if not is_supported:
            raise BootstrapError(f"Language '{instance.language}' not supported for execution environment.")
        # Force runtime rebuild when setup is updated/rebuilt
        force_runtime = config.force_full_build or config.rerun_metrics

        try:
            # Attempt with agent or reuse
            setup_img = bootstrap_setup_phase(
                client,
                instance,
                metadata,
                config,
                instance_logger,
                use_base_image=not is_supported,
                force_rebuild=config.force_full_build,
                reuse_only=config.rerun_metrics,
            )
            # Save metadata after setup completes
            metadata.save_to_json(metadata_path)
            if is_interrupted[0]:
                instance_logger.warning("Bootstrap interrupted, skipping runtime phase.")
                return False
            bootstrap_runtime_phase(
                client, instance, setup_img, config, instance_logger, metadata=metadata, force=force_runtime
            )
            instance_logger.info(f"✅ Successfully bootstrapped {instance.id}.")

        except (RuntimeError, TimeoutError, BootstrapError) as e:
            raise e  # If you want to allow instances without execution environment, remove this line.
            instance_logger.error(f"Attempt failed for {instance.id} ({e}). Retrying with base image...")
            setup_img = bootstrap_setup_phase(client, instance, metadata, config, instance_logger, use_base_image=True)
            metadata.save_to_json(metadata_path)
            if is_interrupted[0]:
                instance_logger.warning("Bootstrap interrupted, skipping runtime phase.")
                return False
            bootstrap_runtime_phase(
                client, instance, setup_img, config, instance_logger, metadata=metadata, force=force_runtime
            )
            instance_logger.info(f"✅ Successfully bootstrapped {instance.id} on retry.")

        return True

    except Exception as e:
        instance_logger.error(f"❌ FAILED to bootstrap for {instance.id}: {e}")
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
        self.interrupted = [False]

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            sig_name = signal.Signals(signum).name
            self.logger.warning(f"\nReceived {sig_name}, initiating shutdown...")
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self.interrupted[0] = True
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
                executor.submit(bootstrap_single_instance, inst, self.config, self.interrupted): inst
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
