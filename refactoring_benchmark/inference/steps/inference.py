"""Final inference execution step."""

import logging
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
    prepare_temp_task_description,
)
from refactoring_benchmark.utils.models import InstanceRow


class InferenceStep:
    """Handles final inference execution (applies refactoring to codebase)."""

    def __init__(
        self,
        instance: InstanceRow,
        config: InferenceConfig,
        output_dir: Path,
        logger: logging.Logger,
        client,
    ) -> None:
        self.instance = instance
        self.config = config
        self.output_dir = output_dir
        self.logger: logging.Logger = logger
        self.executor = ContainerExecutor(instance, config, output_dir, logger, client)
        self.temp_description_dir: Optional[Path] = None

    def run(self, context: ExecutionContext) -> bool:
        """
        Execute the final inference phase.

        Args:
            context: Execution context with plan/multiplan details

        Returns:
            True if inference completed successfully, False otherwise
        """
        self.logger.info("=== INFERENCE STEP ===")

        # Prepare inference environment
        if not self._prepare_inference_environment(context):
            return False

        # Execute container
        if not self.executor.run(
            "inference",
            self.config.timeout,
            self.temp_description_dir,
            context=context,
        ):
            self.logger.error("Inference step failed")
            return False

        # Validate outputs
        return self._validate_outputs(context)

    def _prepare_inference_environment(
        self,
        context: ExecutionContext,
    ) -> bool:
        """
        Prepare temp description directory for inference step.

        Args:
            context: Execution context with plan/multiplan details

        Returns:
            True if preparation successful, False otherwise
        """
        if context.plan_content:
            # Multiplan mode: use selected plan content
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=None,
                content=context.plan_content,
            )
        elif context.plan_path:
            # Plan mode: use plan file content
            plan_content_from_file = context.plan_path.read_text(encoding="utf-8")
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=None,
                content=plan_content_from_file,
            )
        else:
            # Standard mode: use standard description
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=self.config.description_type,
            )

        if not self.temp_description_dir:
            self.logger.error("Failed to prepare inference description")
            return False
        return True

    def _validate_outputs(
        self,
        context: ExecutionContext,
    ) -> bool:
        """
        Validate that required output files exist and contain valid data.

        Args:
            context: Execution context with plan/multiplan details

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

        # Check C: Load metadata and check success
        metadata: InferenceMetadata = InferenceMetadata.load_from_json(metadata_path)
        is_success = metadata.finish_reason.lower() == "success"

        # Set description_type with appropriate suffix
        metadata.description_type = context.full_description_type
        metadata.save_to_json(metadata_path)

        if is_success:
            self.logger.info("Inference completed successfully")
        else:
            self.logger.error(f"Inference failed with reason: {metadata.finish_reason} {metadata.additional}")

        return is_success

    def cleanup_temp_dir(self) -> None:
        """Clean up temporary description directory."""
        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)
            self.temp_description_dir = None
