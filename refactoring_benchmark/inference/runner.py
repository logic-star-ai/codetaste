import shutil
from pathlib import Path
import time
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.inference.models import InferenceConfig, InferenceMetadata
from refactoring_benchmark.inference.utils import (
    copy_agent_config,
    create_fallback_inference_metadata,
    get_instance_output_dir,
    output_exists,
    cleanup_temp_dir,
    output_container_logs,
    prepare_temp_task_description,
    prepare_temp_plan_description
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
        self.plan_path: Optional[Path] = None

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

    def _check_existing_plan(self) -> bool:
        """
        Check if a successful plan already exists (plan_metadata.json with success status).

        Returns:
            True if successful plan exists and should be reused, False otherwise
        """
        # Plan reuse logic: reuse if (not force) OR reuse_successful_plan
        should_reuse = (not self.config.force) or self.config.reuse_successful_plan
        if not should_reuse:
            self.logger.info("--force specified without --reuse-successful-plan, will generate new plan")
            return False

        plan_metadata_path = self.output_dir / "plan_metadata.json"
        if not plan_metadata_path.exists():
            return False

        try:
            metadata: InferenceMetadata = InferenceMetadata.load_from_json(plan_metadata_path)
            is_success = metadata.finish_reason.lower() == "success"
            if is_success:
                self.logger.info("Found existing successful plan, reusing it")
                # Load the existing refactoring_plan.md
                plan_path = self.output_dir / "refactoring_plan.md"
                if plan_path.exists():
                    self.plan_path = plan_path
                    return True
                else:
                    self.logger.warning("plan_metadata.json exists but refactoring_plan.md missing")
                    return False
            else:
                self.logger.info(f"Found plan_metadata.json with non-success status: {metadata.finish_reason}")
                return False
        except Exception as e:
            self.logger.warning(f"Failed to load plan_metadata.json: {e}")
            return False

    def prepare_environment(self) -> bool:
        """
        Prepare output directory and Podman client.
        Preserves plan_metadata.json and refactoring_plan.md if they exist.

        Returns:
            True if preparation successful, False otherwise
        """
        should_preserve_plans = self.config.plan and (
            (not self.config.force) or self.config.reuse_successful_plan
        )
        saved_plan_metadata = None
        saved_plan_content = None

        if self.output_dir.exists():
            plan_metadata_path = self.output_dir / "plan_metadata.json"
            plan_path = self.output_dir / "refactoring_plan.md"

            if should_preserve_plans and plan_metadata_path.exists() and plan_path.exists():
                saved_plan_metadata = plan_metadata_path.read_text(encoding="utf-8")
                saved_plan_content = plan_path.read_text(encoding="utf-8")

            # Clean output directory
            shutil.rmtree(self.output_dir)

        # Create fresh output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        copy_agent_config(self.config.agent_dir, self.output_dir)

        if saved_plan_metadata and saved_plan_content:
            (self.output_dir / "plan_metadata.json").write_text(saved_plan_metadata, encoding="utf-8")
            (self.output_dir / "refactoring_plan.md").write_text(saved_plan_content, encoding="utf-8")

        # Connect to Podman
        self.client = podman_utils.get_local_client(timeout=self.config.timeout + 120)
        if not self.client:
            self.logger.error("Failed to connect to Podman")
            return False
        return True

    def prepare_plan_environment(self) -> bool:
        """
        Prepare temp description directory for planning step.

        Returns:
            True if preparation successful, False otherwise
        """
        self.temp_description_dir = prepare_temp_plan_description(
            self.instance,
            logger=self.logger,
            description_type=self.config.description_type,
        )
        if not self.temp_description_dir:
            self.logger.error("Failed to prepare plan description")
            return False
        return True

    def prepare_inference_environment(self) -> bool:
        """
        Prepare temp description directory for inference step.
        Uses plan content if plan mode is active, otherwise uses standard description.

        Returns:
            True if preparation successful, False otherwise
        """
        # Clean up old temp directory if it exists
        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)
            self.temp_description_dir = None

        if self.plan_path:
            plan_content = self.plan_path.read_text(encoding="utf-8")
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=None,
                content=plan_content,
            )
        else:
            # Use standard task description
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=self.config.description_type,
            )

        if not self.temp_description_dir:
            self.logger.error("Failed to prepare inference description")
            return False
        return True

    def _execute_container_step(self, mode: str, timeout: int) -> bool:
        """
        Execute a container step (either "plan" or "inference").

        Args:
            mode: Container execution mode ("plan" or "inference")
            timeout: Timeout in seconds for this step

        Returns:
            True if container executed without errors, False otherwise
        """
        self.logger.info(f"Starting {mode} step for {self.instance.display_path}")
        self.logger.info(f"  Image: {self.instance.runtime_image}")
        self.logger.info(f"  Timeout: {timeout}s")

        env = {**self.config.env_vars, "DESCRIPTION_TYPE": self.config.description_type}
        try:
            # Run container
            self.container = podman_utils.safe_container_run(
                self.client,
                self.instance.runtime_image,
                command=[mode],  # "plan" or "inference"
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
                self.container.wait(timeout=timeout)
            except Exception as e:
                self.logger.error(f"{mode.capitalize()} step timed out: {e}")
                finish_reason = "error_planmode" if mode == "plan" else "timeout"
                create_fallback_inference_metadata(
                    self.output_dir,
                    finish_reason,
                    description_type=self.config.description_type,
                    additional={"error": f"{mode.capitalize()} container timed out: {str(e)}"},
                )
                return False

            # Output logs
            log_file = f"{mode}.out"
            output_container_logs(self.container, self.output_dir / log_file, self.logger)
            return True

        except Exception as e:
            self.logger.error(f"{mode.capitalize()} step execution failed: {e}")
            return False
        finally:
            self.container_cleanup()

    def _validate_plan_output(self) -> bool:
        """Validate that plan step created a valid refactoring_plan.md."""
        plan_path = self.output_dir / "refactoring_plan.md"
        error = None
        if not plan_path.exists():
            error = "Agent did not produce refactoring_plan.md during plan step"
        elif plan_path.stat().st_size < 10:
            error = "refactoring_plan.md is empty or too small"

        if error:
            self.logger.error(f"Plan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir, "error_planmode",
                description_type=self.config.description_type,
                additional={"error": error},
            )
            return False
        self.logger.info(f"Plan validation successful: {plan_path.stat().st_size} bytes")
        self.plan_path = plan_path

        # Rename inference_metadata.json to plan_metadata.json after successful plan
        inference_metadata_path = self.output_dir / "inference_metadata.json"
        plan_metadata_path = self.output_dir / "plan_metadata.json"
        if inference_metadata_path.exists():
            try:
                inference_metadata_path.rename(plan_metadata_path)
                self.logger.info("Renamed inference_metadata.json to plan_metadata.json")
            except Exception as e:
                self.logger.warning(f"Failed to rename inference_metadata.json to plan_metadata.json: {e}")

        return True

    def execute_plan(self) -> bool:
        """
        Execute the planning step (creates refactoring_plan.md from task description).

        Returns:
            True if planning step completed without errors, False otherwise
        """
        self.logger.info("=== PLAN STEP ===")
        if not self._execute_container_step("plan", timeout=self.config.plan_timeout):
            self.logger.error("Plan step failed - aborting")
            return False
        return True

    def execute_inference(self) -> bool:
        """
        Execute the inference step (applies refactoring to codebase).

        Returns:
            True if execution completed without errors, False otherwise
        """
        self.logger.info("=== INFERENCE STEP ===")
        if not self._execute_container_step("inference", timeout=self.config.timeout):
            self.logger.error("Inference step failed")
            return False
        return True

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
        metadata: InferenceMetadata = InferenceMetadata.load_from_json(metadata_path)
        is_success = metadata.finish_reason.lower() == "success"
        metadata.description_type = self.config.description_type
        metadata.save_to_json(metadata_path)

        if is_success:
            self.logger.info("Inference completed successfully")
        else:
            self.logger.error(f"Inference failed with reason: {metadata.finish_reason} {metadata.additional}")

        return is_success

    def container_cleanup(self) -> None:
        if self.container:
            podman_utils.stop_container(self.container)
            try:
                self.container.remove(force=True)
            except Exception as e:
                self.logger.warning(
                    f"Failed to remove container [{self.instance.id}]. Probably already removed. Error: {e}"
                )
            self.container = None

    def cleanup(self) -> None:
        """Clean up container and temporary files."""
        self.container_cleanup()
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
            # Phase 2: Prepare base environment (output dir, podman)
            if not self.prepare_environment():
                return False

            # Phase 3: Plan step (if enabled)
            if self.config.plan:
                # Check if successful plan already exists
                if not self._check_existing_plan():
                    # Need to run plan step
                    if not self.prepare_plan_environment():
                        return False
                    if not self.execute_plan():
                        return False
                    if not self._validate_plan_output():
                        return False
                else:
                    self.logger.info("Skipping plan execution, using existing plan")

            # Phase 4: Inference step (always executed, description depends on plan mode)
            if not self.prepare_inference_environment():
                return False
            if not self.execute_inference():
                return False

            # Phase 5: Validate outputs
            return self.validate_outputs()

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
        finally:
            self.cleanup()
