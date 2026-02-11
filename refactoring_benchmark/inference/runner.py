"""Main orchestrator for instance inference execution."""

import shutil
from pathlib import Path
from typing import Optional

import podman

from refactoring_benchmark.inference.models import (
    InferenceConfig,
    InferenceMetadata,
)
from refactoring_benchmark.inference.steps.plan import PlanStep
from refactoring_benchmark.inference.steps.multiplan import MultiplanStep
from refactoring_benchmark.inference.steps.inference import InferenceStep
from refactoring_benchmark.inference.utils import (
    build_context,
    copy_agent_config,
    get_instance_output_dir,
    output_exists,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow


class InstanceInferenceRunner:
    """Orchestrates the phases of running inference on a single instance."""

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
            f"{instance.id}",
            use_file=True,
            use_stdout=False,
            log_subdir=f"{config.sanitized_agent_id}",
        )
        self.output_dir = get_instance_output_dir(instance, config.sanitized_agent_id, config.output_dir)
        self.client: Optional[podman.PodmanClient] = None

    def should_skip(self) -> tuple[bool, bool]:
        """
        Check if instance should be skipped (output already exists).

        Returns:
            Tuple of (should_skip, is_success)
        """
        if self.config.force:
            return False, False

        if not output_exists(self.output_dir):
            return False, False

        metadata_path = self.output_dir / "inference_metadata.json"
        is_success = False
        metadata_loaded = False

        try:
            metadata: InferenceMetadata = InferenceMetadata.load_from_json(metadata_path)
            is_success = metadata.finish_reason.lower() == "success"
            metadata_loaded = True
        except Exception:
            self.logger.warning("Failed to read metadata. " f"Skipping = {not self.config.force_unsuccessful}.")

        if self.config.force_unsuccessful:
            should_skip = is_success
        else:
            should_skip = metadata_loaded

        if should_skip:
            self.logger.info(f"Skipping {self.instance.id}, output already exists.")

        return should_skip, is_success

    def prepare_environment(self) -> bool:
        """
        Cleans output directory. If reusing plans, saves and restores them.

        Returns:
            True if preparation successful, False otherwise
        """
        # reuse plans for non-forced inference or if reusing successful plans
        should_preserve_plans = self.config.mode == "plan" and (
            (not self.config.force) or self.config.reuse_successful_plan
        )
        should_preserve_multiplan = self.config.mode == "multiplan" and (
            (not self.config.force) or self.config.reuse_successful_plan
        )
        saved_plan_metadata = None
        saved_plan_content = None
        saved_multiplan_metadata = None
        saved_multiplan_plans = {}

        if self.output_dir.exists():
            # Save plan files if needed
            if should_preserve_plans:
                plan_metadata_path = self.output_dir / "plan_metadata.json"
                plan_path = self.output_dir / "refactoring_plan.md"
                if plan_metadata_path.exists() and plan_path.exists():
                    saved_plan_metadata = plan_metadata_path.read_text(encoding="utf-8")
                    saved_plan_content = plan_path.read_text(encoding="utf-8")

            # Save multiplan files if needed
            if should_preserve_multiplan:
                multiplan_metadata_path = self.output_dir / "multiplan_metadata.json"
                plans_dir = self.output_dir / "refactoring_plans"
                if multiplan_metadata_path.exists() and plans_dir.exists():
                    saved_multiplan_metadata = multiplan_metadata_path.read_text(encoding="utf-8")
                    from refactoring_benchmark.inference.utils import NUM_MULTIPLAN

                    for i in range(NUM_MULTIPLAN):
                        plan_path = plans_dir / f"refactoring_plan{i}.md"
                        if plan_path.exists():
                            saved_multiplan_plans[i] = plan_path.read_text(encoding="utf-8")

            # Clean output directory
            shutil.rmtree(self.output_dir)

        # Create fresh output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        copy_agent_config(self.config.agent_dir, self.output_dir)

        # Restore plan files if they were saved
        if saved_plan_metadata and saved_plan_content:
            (self.output_dir / "plan_metadata.json").write_text(saved_plan_metadata, encoding="utf-8")
            (self.output_dir / "refactoring_plan.md").write_text(saved_plan_content, encoding="utf-8")

        # Restore multiplan files if they were saved
        if saved_multiplan_metadata and saved_multiplan_plans:
            (self.output_dir / "multiplan_metadata.json").write_text(saved_multiplan_metadata, encoding="utf-8")
            plans_dir = self.output_dir / "refactoring_plans"
            plans_dir.mkdir(exist_ok=True)
            for i, content in saved_multiplan_plans.items():
                (plans_dir / f"refactoring_plan{i}.md").write_text(content, encoding="utf-8")

        # Connect to Podman
        self.client = podman_utils.get_local_client(timeout=self.config.timeout + 120)
        if not self.client:
            self.logger.error("Failed to connect to Podman")
            return False
        return True

    def cleanup(self) -> None:
        """Clean up Podman client."""
        if self.client:
            self.client.close()

    def run(self) -> bool:
        """
        Execute all phases in order: Plan or Multiplan -> Inference.

        Returns:
            True if inference completed successfully, False otherwise
        """
        # Phase 1: Skip check
        should_skip, is_success = self.should_skip()
        if should_skip:
            return is_success

        try:
            # Phase 2: Prepare base environment (output dir, podman). Remove old output.
            if not self.prepare_environment():
                return False

            plan_path: Optional[Path] = None
            plan_content: Optional[str] = None

            # Phase 3: Plan step (if enabled)
            step_map = {
                "plan": (PlanStep, "plan_path"),
                "multiplan": (MultiplanStep, "plan_content"),
            }
            step_entry = step_map.get(self.config.mode)
            if step_entry:
                step_cls, payload_key = step_entry
                step: PlanStep | MultiplanStep = step_cls(self.instance, self.config, self.output_dir, self.logger, self.client)
                try:
                    payload = step.run()
                    if not payload:
                        return False
                    if payload_key == "plan_path":
                        plan_path = payload
                    else:
                        plan_content = payload
                finally:
                    step.cleanup_temp_dir()

            # Phase 4: Inference step (always executed)
            if plan_content:
                self.logger.info("Using multiplan content for inference.")
            elif plan_path:
                self.logger.info(f"Using plan file for inference. {plan_path}")
            context = build_context(self.config, plan_path=plan_path, plan_content=plan_content)

            inference_step = InferenceStep(self.instance, self.config, self.output_dir, self.logger, self.client)
            try:
                return inference_step.run(context)
            finally:
                inference_step.cleanup_temp_dir()

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
        finally:
            self.cleanup()
