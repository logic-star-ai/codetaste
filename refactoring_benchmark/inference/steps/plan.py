"""Single plan generation step."""

from pathlib import Path
from typing import Optional

from refactoring_benchmark.inference.models import (
    ExecutionContext,
    InferenceConfig,
    InferenceMetadata,
)
from refactoring_benchmark.inference.steps.executor import ContainerExecutor
from refactoring_benchmark.inference.utils import (
    cleanup_temp_dir,
    prepare_temp_plan_description,
    create_fallback_inference_metadata,
)
from refactoring_benchmark.utils.models import InstanceRow


class PlanStep:
    """Handles single plan generation (refactoring_plan.md)."""

    def __init__(
        self,
        instance: InstanceRow,
        config: InferenceConfig,
        output_dir: Path,
        logger,
        client,
    ) -> None:
        self.instance = instance
        self.config = config
        self.output_dir = output_dir
        self.logger = logger
        self.executor = ContainerExecutor(
            instance, config, output_dir, logger, client
        )
        self.temp_description_dir: Optional[Path] = None

    def run(self) -> Optional[Path]:
        """
        Execute the planning step.

        Returns:
            Path to refactoring_plan.md if successful, None otherwise
        """
        # Check if successful plan already exists
        if self._check_existing_plan():
            return self.output_dir / "refactoring_plan.md"

        self.logger.info("=== PLAN STEP ===")

        # Prepare plan description
        self.temp_description_dir = prepare_temp_plan_description(
            self.instance,
            logger=self.logger,
            description_type=self.config.description_type,
        )
        if not self.temp_description_dir:
            self.logger.error("Failed to prepare plan description")
            return None

        # Execute container
        context = ExecutionContext(
            description_type=self.config.description_type,
            description_type_suffix="_plan",
        )
        if not self.executor.run(
            "plan",
            self.config.plan_timeout,
            self.temp_description_dir,
            context=context,
        ):
            self.logger.error("Plan step failed - aborting")
            return None

        # Validate output
        if not self._validate_plan_output(context):
            return None

        return self.output_dir / "refactoring_plan.md"

    def cleanup_temp_dir(self) -> None:
        """Clean up temporary description directory."""
        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)
            self.temp_description_dir = None

    def _check_existing_plan(self) -> bool:
        """
        Check if a successful plan already exists.

        Returns:
            True if successful plan exists and should be reused, False otherwise
        """
        # Plan reuse logic: reuse if (not force) OR reuse_successful_plan
        should_reuse = (not self.config.force) or self.config.reuse_successful_plan
        if not should_reuse:
            self.logger.info(
                "--force specified without --reuse-successful-plan, will generate new plan"
            )
            return False

        plan_metadata_path = self.output_dir / "plan_metadata.json"
        if not plan_metadata_path.exists():
            return False

        try:
            metadata: InferenceMetadata = InferenceMetadata.load_from_json(
                plan_metadata_path
            )
            is_success = metadata.finish_reason.lower() == "success"
            if is_success:
                self.logger.info("Found existing successful plan, reusing it")
                # Verify refactoring_plan.md exists
                plan_path = self.output_dir / "refactoring_plan.md"
                if plan_path.exists():
                    return True
                else:
                    self.logger.warning(
                        "plan_metadata.json exists but refactoring_plan.md missing"
                    )
                    return False
            else:
                self.logger.info(
                    f"Found plan_metadata.json with non-success status: {metadata.finish_reason}"
                )
                return False
        except Exception as e:
            self.logger.warning(f"Failed to load plan_metadata.json: {e}")
            return False

    def _validate_plan_output(self, context: ExecutionContext) -> bool:
        """
        Validate that plan step created a valid refactoring_plan.md.

        Returns:
            True if validation successful, False otherwise
        """
        plan_path = self.output_dir / "refactoring_plan.md"
        error = None

        if not plan_path.exists():
            error = "Agent did not produce refactoring_plan.md during plan step"
        elif plan_path.stat().st_size < 10:
            error = "refactoring_plan.md is empty or too small"

        if error:
            self.logger.error(f"Plan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir,
                "error_planmode",
                description_type=context.full_description_type,
                additional={"error": error},
            )
            return False

        self.logger.info(f"Plan validation successful: {plan_path.stat().st_size} bytes")

        # Rename inference_metadata.json to plan_metadata.json after successful plan
        inference_metadata_path = self.output_dir / "inference_metadata.json"
        plan_metadata_path = self.output_dir / "plan_metadata.json"
        if inference_metadata_path.exists():
            try:
                inference_metadata_path.rename(plan_metadata_path)
                inference_metadata: InferenceMetadata = (
                    InferenceMetadata.load_from_json(plan_metadata_path)
                )
                inference_metadata.description_type = context.full_description_type
                inference_metadata.save_to_json(plan_metadata_path)
                self.logger.info(
                    "Renamed inference_metadata.json to plan_metadata.json"
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to rename inference_metadata.json to plan_metadata.json: {e}"
                )

        return True
