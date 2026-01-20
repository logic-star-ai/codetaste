import shutil
from pathlib import Path
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.inference.models import InferenceConfig, InferenceMetadata
from refactoring_benchmark.inference.utils import (
    copy_agent_config,
    create_fallback_inference_metadata,
    get_instance_output_dir,
    output_exists,
    prepare_temp_description,
    cleanup_temp_dir,
    output_container_logs,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow


class InstanceInferenceRunner:
    """Encapsulates the phases of running inference on a single instance."""

    def __init__(self, instance: InstanceRow, config: InferenceConfig):
        """
        Initialize the runner for a single instance.

        Args:
            instance: Instance row from CSV
            config: Inference configuration
        """
        self.instance = instance
        self.config = config
        self.logger = get_logger(
            f"{instance.id}", use_file=True, use_stdout=False, log_subdir=f"{config.sanitized_agent_id}"
        )
        self.output_dir = get_instance_output_dir(instance, config.sanitized_agent_id, config.output_dir)
        self.container: Optional[PodmanContainer] = None
        self.temp_description_dir: Optional[Path] = None
        self.client: Optional[podman.PodmanClient] = None

    def should_skip(self) -> tuple[bool, bool]:
        """
        Check if instance should be skipped (output already exists).

        Returns:
            Tuple of (should_skip, is_success)
        """
        if output_exists(self.output_dir) and not self.config.force:
            self.logger.info(f"Skipping {self.instance.id}, output already exists.")
            try:
                metadata: InferenceMetadata = InferenceMetadata.load_from_json(
                    self.output_dir / "inference_metadata.json"
                )
                is_success = metadata.finish_reason.lower() == "success"
                if is_success or not self.config.force_unsuccessful:
                    return True, is_success
            except Exception:
                return True, False
        return False, False

    def prepare_environment(self) -> bool:
        """
        Prepare output directory, agent config, and temp description directory.

        Returns:
            True if preparation successful, False otherwise
        """
        # Clean and create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        copy_agent_config(self.config.agent_dir, self.output_dir)

        # Connect to Podman
        self.client = podman_utils.get_local_client(timeout=self.config.timeout + 120)
        if not self.client:
            self.logger.error("Failed to connect to Podman")
            return False

        # Prepare temp description directory
        try:
            self.temp_description_dir = prepare_temp_description(
                self.instance, self.config.description_type, self.logger
            ).resolve()
        except (ValueError, FileNotFoundError) as e:
            self.logger.error(f"Failed to prepare description: {e}")
            return False

        return True

    def execute_container(self) -> bool:
        """
        Execute the inference container.

        Returns:
            True if container executed without errors, False otherwise
        """
        self.logger.info(f"Starting inference for {self.instance.display_path}")
        self.logger.info(f"  Image: {self.instance.runtime_image}")
        self.logger.info(f"  Output: {self.output_dir}")

        env = {**self.config.env_vars, "DESCRIPTION_TYPE": self.config.description_type}
        self.logger.debug(
            f"  Environment Variables: {[(k, v[:10] if isinstance(v, str) else v) for k, v in env.items()]}"
        )

        try:
            # Run container
            self.container = podman_utils.safe_container_run(
                self.client,
                self.instance.runtime_image,
                command=["inference"],
                detach=True,
                environment=env,
                volumes={
                    str(self.config.agent_dir): {"bind": "/agent", "mode": "rw"},
                    str(self.output_dir): {"bind": "/output", "mode": "rw"},
                    str(self.temp_description_dir): {
                        "bind": "/task_description",
                        "mode": "rw",
                        "extended_mode": ["U", "z"],
                    },
                },
                network_mode="host",
                working_dir="/testbed",
                remove=False,
                nano_cpus=int(8e9),
            )

            # Wait for completion
            try:
                self.container.wait(timeout=self.config.timeout)
            except Exception as e:
                self.logger.error(f"Execution timed out: {e}")
                create_fallback_inference_metadata(
                    self.output_dir,
                    "timeout",
                    description_type=self.config.description_type,
                    additional={"error": f"Container timed out: {str(e)}"},
                )

            # Output logs
            output_container_logs(self.container, self.output_dir / "inference.out", self.logger)
            return True

        except Exception as e:
            self.logger.error(f"Container execution failed: {e}")
            return False

    def validate_outputs(self) -> bool:
        """
        Validate that required output files exist and contain valid data.

        Returns:
            True if validation successful (finish_reason == success), False otherwise
        """
        metadata_path = self.output_dir / "inference_metadata.json"
        prediction_path = self.output_dir / "prediction.diff"

        # Check A: Metadata exists
        if not metadata_path.exists():
            self.logger.error("Agent failed to create inference_metadata.json")
            return False

        # Check B: Prediction exists
        if not prediction_path.exists():
            self.logger.error("Agent or entrypoint.sh failed to generate / create prediction.diff")
            return False

        # Check C: Success reason
        metadata = InferenceMetadata.load_from_json(metadata_path)
        is_success = metadata.finish_reason.lower() == "success"
        metadata.description_type = self.config.description_type
        metadata.save_to_json(metadata_path)

        if is_success:
            self.logger.info("Inference completed successfully")
        else:
            self.logger.error(f"Inference failed with reason: {metadata.finish_reason} {metadata.additional}")

        return is_success

    def cleanup(self) -> None:
        """Clean up container and temporary files."""
        if self.container:
            podman_utils.stop_container(self.container)
            try:
                self.container.remove(force=True)
            except Exception as e:
                self.logger.warning(
                    f"Failed to remove container [{self.instance.id}]. Probably already removed. Error: {e}"
                )

        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)

        if self.client:
            self.client.close()

    def run(self) -> bool:
        """
        Execute all phases in order.

        Returns:
            True if inference completed successfully, False otherwise
        """
        # Phase 1: Skip check
        should_skip, is_success = self.should_skip()
        if should_skip:
            return is_success

        try:
            # Phase 2: Prepare environment
            if not self.prepare_environment():
                return False

            # Phase 3: Execute container
            if not self.execute_container():
                return False

            # Phase 4: Validate outputs
            return self.validate_outputs()

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
        finally:
            # Phase 5: Cleanup
            self.cleanup()
