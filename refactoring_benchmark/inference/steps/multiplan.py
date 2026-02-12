"""Multi-plan generation and judging step."""

import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from refactoring_benchmark.inference.judge import judge_best_plan
from refactoring_benchmark.inference.models import (ExecutionContext,
                                                    InferenceConfig,
                                                    MultiplanMetadata)
from refactoring_benchmark.inference.steps.executor import ContainerExecutor
from refactoring_benchmark.inference.utils import (
    NUM_MULTIPLAN, build_context, cleanup_temp_dir,
    create_fallback_inference_metadata, finalize_step_metadata,
    prepare_temp_multiplan_description)
from refactoring_benchmark.utils.models import InstanceRow

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MultiplanStep:
    """Handles multi-plan generation and LLM judging."""

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
        self.executor = ContainerExecutor(instance, config, output_dir, logger, client)
        self.temp_description_dir: Optional[Path] = None
        self.selected_plan_content: Optional[str] = None
        self.multiplan_metadata: Optional[MultiplanMetadata] = None

    def run(self) -> Optional[str]:
        """
        Execute the multiplan generation and judging step.

        Returns:
            Content of the selected plan if successful, None otherwise
        """
        # Check if successful multiplan already exists
        if self._check_existing_multiplan():
            return self.selected_plan_content

        self.logger.info("=== MULTIPLAN STEP ===")

        # Track start time for metadata
        multiplan_start_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        # Prepare multiplan description
        self.temp_description_dir = prepare_temp_multiplan_description(
            self.instance,
            logger=self.logger,
            description_type=self.config.description_type,
        )
        if not self.temp_description_dir:
            self.logger.error("Failed to prepare multiplan description")
            return None

        # Execute container to generate multiple plans
        context = build_context(self.config, mode="multiplan")
        if not self.executor.run(
            "multiplan",
            self.config.plan_timeout,
            self.temp_description_dir,
            context=context,
        ):
            self.logger.error("Multiplan step failed - aborting")
            return None

        # Validate that all plans were created
        if not self._validate_multiplan_output(context):
            return None

        # Execute judge to select best plan
        try:
            selected_index, judge_metadata = self._execute_judge()
            self.logger.info(f"Judge selected plan index: {selected_index}")
            self._save_multiplan_metadata(selected_index, judge_metadata, multiplan_start_time)
            self._load_selected_plan(selected_index)
            return self.selected_plan_content
        except Exception as e:
            self.logger.error(f"Judge execution failed: {e}")
            create_fallback_inference_metadata(
                self.output_dir,
                "error_judge",
                description_type=context.description_type,
                mode=context.mode,
                additional={"error": str(e)},
            )
            return None

    def cleanup_temp_dir(self) -> None:
        """Clean up temporary description directory."""
        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)
            self.temp_description_dir = None

    def _check_existing_multiplan(self) -> bool:
        """
        Check if a successful multiplan result already exists.

        Returns:
            True if successful multiplan exists and should be reused, False otherwise
        """
        should_reuse = (not self.config.force) or self.config.reuse_successful_plan
        if not should_reuse:
            self.logger.info("--force specified without --reuse-successful-plan, will generate new multiplan")
            return False

        multiplan_metadata_path = self.output_dir / "multiplan_metadata.json"
        if not multiplan_metadata_path.exists():
            return False

        try:
            metadata = MultiplanMetadata.load_from_json(multiplan_metadata_path)
            if metadata.finish_reason.lower() != "success" or metadata.selected_plan_index is None:
                self.logger.info(f"Found multiplan_metadata.json with status: {metadata.finish_reason}")
                return False

            self.logger.info("Found existing successful multiplan, verifying plans...")
            plans_dir = self.output_dir / "refactoring_plans"
            if all((plans_dir / f"refactoring_plan{i}.md").exists() for i in range(NUM_MULTIPLAN)):
                self._load_selected_plan(metadata.selected_plan_index)
                self.multiplan_metadata = metadata
                return True

            self.logger.warning("multiplan_metadata.json exists but some plans are missing")
            return False
        except Exception as e:
            self.logger.warning(f"Failed to load multiplan_metadata.json: {e}")
            return False

    def _validate_multiplan_output(self, context: ExecutionContext) -> bool:
        """
        Validate that multiplan step created expected number of valid plan files.

        Returns:
            True if validation successful, False otherwise
        """
        plans_dir = self.output_dir / "refactoring_plans"

        if not plans_dir.exists():
            error = "refactoring_plans directory does not exist"
            self.logger.error(f"Multiplan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir,
                "error_multiplan",
                description_type=context.description_type,
                mode=context.mode,
                additional={"error": error},
            )
            return False

        # Check for expected plans
        expected_plans = {f"refactoring_plan{i}.md" for i in range(NUM_MULTIPLAN)}
        missing = [name for name in expected_plans if not (plans_dir / name).exists()]
        small = [
            name for name in expected_plans if (plans_dir / name).exists() and (plans_dir / name).stat().st_size < 10
        ]

        if missing or small:
            errors = [
                f"missing: {', '.join(missing)}" if missing else None,
                f"empty/small: {', '.join(small)}" if small else None,
            ]
            error = f"Invalid plans ({'; '.join(filter(None, errors))})"
            self.logger.error(f"Multiplan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir,
                "error_multiplan",
                description_type=context.description_type,
                mode=context.mode,
                additional={"error": error},
            )
            return False

        # Rename inference_metadata.json to multiplan_generation_metadata.json
        inference_metadata_path = self.output_dir / "inference_metadata.json"
        multiplan_generation_metadata_path = self.output_dir / "multiplan_generation_metadata.json"
        finalize_step_metadata(
            src=inference_metadata_path,
            dst=multiplan_generation_metadata_path,
            description_type=context.description_type,
            mode=context.mode,
            logger=self.logger,
        )

        return True

    def _execute_judge(self) -> tuple[int, dict]:
        """
        Execute LLM judge to select best plan from candidates.

        Returns:
            Tuple of (selected_plan_index, judge_metadata_dict)

        Raises:
            Exception: If judge execution fails
        """
        self.logger.info("=== JUDGE STEP ===")

        # Load full original description from assets
        description_path = PROJECT_ROOT / self.instance.asset_dir("descriptions") / "description.md"
        original_description = description_path.read_text(encoding="utf-8")
        self.logger.info(f"Loaded full description from {description_path}")

        # Load all candidate plans
        plans_dir = self.output_dir / "refactoring_plans"
        candidate_plans = {
            i: (plans_dir / f"refactoring_plan{i}.md").read_text(encoding="utf-8") for i in range(NUM_MULTIPLAN)
        }

        # Call judge
        try:
            selected_index, judge_metadata = judge_best_plan(original_description, candidate_plans)
            self.logger.info(f"Judge selected plan {selected_index} (cost: ${judge_metadata['judge_cost_usd']:.4f})")

            # Save judge output to file for inspection
            judge_output_path = self.output_dir / "judge.out"
            judge_output_path.write_text(judge_metadata.get("judge_reasoning", ""), encoding="utf-8")
            self.logger.info(f"Saved judge output to {judge_output_path}")

            return selected_index, judge_metadata
        except Exception as e:
            self.logger.error(f"Judge execution failed:\n{traceback.format_exc()}\n\n{e}")
            raise e

    def _save_multiplan_metadata(self, selected_index: int, judge_metadata: dict, start_time: str) -> None:
        """
        Save multiplan metadata to multiplan_metadata.json.

        Args:
            selected_index: Index of the selected plan
            judge_metadata: Metadata from the judge execution
            start_time: Start time of the multiplan step
        """
        multiplan_metadata = MultiplanMetadata(
            start_time=start_time,
            finish_time=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            finish_reason="success",
            plans_generated=NUM_MULTIPLAN,
            selected_plan_index=selected_index,
            judge_reasoning=judge_metadata.get("judge_reasoning"),
            judge_cost_usd=judge_metadata.get("judge_cost_usd"),
            judge_latency_seconds=judge_metadata.get("judge_latency_seconds"),
            judge_input_tokens=judge_metadata.get("judge_input_tokens"),
            judge_output_tokens=judge_metadata.get("judge_output_tokens"),
        )

        metadata_path = self.output_dir / "multiplan_metadata.json"
        multiplan_metadata.save_to_json(metadata_path)
        self.logger.info(f"Saved multiplan metadata to {metadata_path}")
        self.multiplan_metadata = multiplan_metadata

    def _load_selected_plan(self, selected_index: int) -> None:
        """
        Load the selected plan content for use in inference step.

        Args:
            selected_index: Index of the plan to load
        """
        plans_dir = self.output_dir / "refactoring_plans"
        selected_plan_path = plans_dir / f"refactoring_plan{selected_index}.md"
        self.selected_plan_content = selected_plan_path.read_text(encoding="utf-8")
        self.logger.info(f"Loaded selected plan {selected_index} ({len(self.selected_plan_content)} chars)")
