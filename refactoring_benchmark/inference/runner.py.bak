from datetime import timezone
import shutil
from pathlib import Path
import traceback
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.inference.models import InferenceConfig, InferenceMetadata, MultiplanMetadata
from refactoring_benchmark.inference.judge import judge_best_plan
from refactoring_benchmark.inference.utils import (
    copy_agent_config,
    create_fallback_inference_metadata,
    get_instance_output_dir,
    output_exists,
    cleanup_temp_dir,
    output_container_logs,
    prepare_temp_task_description,
    prepare_temp_plan_description,
    prepare_temp_multiplan_description,
    NUM_MULTIPLAN,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceRow
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
        self.selected_plan_content: Optional[str] = None
        self.multiplan_metadata: Optional[MultiplanMetadata] = None

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
        Uses selected plan content if multiplan mode is active,
        uses plan content if plan mode is active, otherwise uses standard description.

        Returns:
            True if preparation successful, False otherwise
        """
        # Clean up old temp directory if it exists
        if self.temp_description_dir:
            cleanup_temp_dir(self.temp_description_dir, self.logger)
            self.temp_description_dir = None

        if self.selected_plan_content:
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=None,
                content=self.selected_plan_content,
            )
        elif self.plan_path:
            plan_content = self.plan_path.read_text(encoding="utf-8")
            self.temp_description_dir = prepare_temp_task_description(
                self.instance,
                logger=self.logger,
                description_type=None,
                content=plan_content,
            )
        else:
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
                description_type = self.config.description_type
                if self.plan_path:
                    description_type = f"{description_type}_plan"
                create_fallback_inference_metadata(
                    self.output_dir,
                    finish_reason,
                    description_type=description_type,
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
                description_type=self.config.description_type + "_plan",
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
                inference_metadata: InferenceMetadata = InferenceMetadata.load_from_json(plan_metadata_path)
                inference_metadata.description_type = self.config.description_type + "_plan"
                inference_metadata.save_to_json(plan_metadata_path)
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

    # ===== MULTIPLAN MODE METHODS =====
    def prepare_multiplan_environment(self) -> bool:
        """
        Prepare temp description directory for multiplan description.

        Returns:
            True if preparation successful, False otherwise
        """
        self.temp_description_dir = prepare_temp_multiplan_description(
            self.instance,
            logger=self.logger,
            description_type=self.config.description_type,
        )
        if not self.temp_description_dir:
            self.logger.error("Failed to prepare multiplan description")
            return False
        return True

    def execute_multiplan(self) -> bool:
        """
        Execute the multiplan generation step (creates 5 refactoring plans).

        Returns:
            True if multiplan step completed without errors, False otherwise
        """
        self.logger.info("=== MULTIPLAN STEP ===")
        if not self._execute_container_step("multiplan", timeout=self.config.plan_timeout):
            self.logger.error("Multiplan step failed - aborting")
            return False
        return True

    def _validate_multiplan_output(self) -> bool:
        """Validate that multiplan step created expected number of valid plan files."""
        plans_dir = self.output_dir / "refactoring_plans"

        if not plans_dir.exists():
            error = "refactoring_plans directory does not exist"
            self.logger.error(f"Multiplan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir, "error_multiplan",
                description_type=self.config.description_type + "_multiplan",
                additional={"error": error}
            )
            return False

        # Check for expected plans
        expected_plans = {f"refactoring_plan{i}.md" for i in range(NUM_MULTIPLAN)}
        missing = [name for name in expected_plans if not (plans_dir / name).exists()]
        small = [name for name in expected_plans if (plans_dir / name).exists() and (plans_dir / name).stat().st_size < 10]

        if missing or small:
            errors = [f"missing: {', '.join(missing)}" if missing else None,
                     f"empty/small: {', '.join(small)}" if small else None]
            error = f"Invalid plans ({'; '.join(filter(None, errors))})"
            self.logger.error(f"Multiplan step failed: {error}")
            create_fallback_inference_metadata(
                self.output_dir, "error_multiplan",
                description_type=self.config.description_type + "_multiplan",
                additional={"error": error}
            )
            return False

        # Rename inference_metadata.json to multiplan_generation_metadata.json after successful multiplan
        inference_metadata_path = self.output_dir / "inference_metadata.json"
        multiplan_generation_metadata_path = self.output_dir / "multiplan_generation_metadata.json"
        if inference_metadata_path.exists():
            try:
                inference_metadata_path.rename(multiplan_generation_metadata_path)
                inference_metadata: InferenceMetadata = InferenceMetadata.load_from_json(multiplan_generation_metadata_path)
                inference_metadata.description_type = self.config.description_type + "_multiplan"
                inference_metadata.save_to_json(multiplan_generation_metadata_path)
                self.logger.info("Renamed inference_metadata.json to multiplan_generation_metadata.json")
            except Exception as e:
                self.logger.warning(f"Failed to rename inference_metadata.json to multiplan_generation_metadata.json: {e}")

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

        # Load all candidate plans dynamically
        plans_dir = self.output_dir / "refactoring_plans"
        candidate_plans = {
            i: (plans_dir / f"refactoring_plan{i}.md").read_text(encoding="utf-8")
            for i in range(NUM_MULTIPLAN)
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
        """Save multiplan metadata to multiplan_metadata.json."""

        multiplan_metadata = MultiplanMetadata(
            start_time=start_time,
            finish_time=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
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
        """Load the selected plan content for use in inference step."""
        plans_dir = self.output_dir / "refactoring_plans"
        selected_plan_path = plans_dir / f"refactoring_plan{selected_index}.md"
        self.selected_plan_content = selected_plan_path.read_text(encoding="utf-8")
        self.logger.info(f"Loaded selected plan {selected_index} ({len(self.selected_plan_content)} chars)")

    def _check_existing_multiplan(self) -> bool:
        """
        Check if a successful multiplan result already exists.

        Returns:
            True if successful multiplan exists and should be reused, False otherwise
        """
        if not ((not self.config.force) or self.config.reuse_successful_plan):
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

        # Set description_type with _multiplan or _plan suffix if used
        description_type = self.config.description_type
        if self.selected_plan_content:  # Multiplan was used for inference
            description_type = f"{description_type}_multiplan"
        elif self.plan_path:  # Plan was used for inference
            description_type = f"{description_type}_plan"
        metadata.description_type = description_type
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

            # Phase 3.5: Multiplan step (if enabled)
            if self.config.multiplan:
                # Check if successful multiplan already exists
                if not self._check_existing_multiplan():
                    # Need to run multiplan step
                    multiplan_start_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

                    if not self.prepare_multiplan_environment():
                        return False
                    if not self.execute_multiplan():
                        return False
                    if not self._validate_multiplan_output():
                        return False

                    # Execute judge to select best plan
                    try:
                        selected_index, judge_metadata = self._execute_judge()
                        self.logger.info(f"Judge selected plan index: {selected_index}")
                        self._save_multiplan_metadata(selected_index, judge_metadata, multiplan_start_time)
                        self._load_selected_plan(selected_index)
                    except Exception as e:
                        self.logger.error(f"Judge execution failed: {e}")
                        create_fallback_inference_metadata(
                            self.output_dir,
                            "error_judge",
                            description_type=self.config.description_type + "_multiplan",
                            additional={"error": str(e)},
                        )
                        return False
                else:
                    self.logger.info("Skipping multiplan execution, using existing multiplan result")

            # Phase 4: Inference step (always executed, description depends on plan/multiplan mode)
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
