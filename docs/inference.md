# Inference Behavior (Concise)

This document summarizes how inference runs for a single instance.

## Phases
1. **Skip check**
   - If `prediction.diff` exists and `--force` is not set, the instance is skipped.
   - If skipped and `finish_reason=success`, the run returns **success**.
   - If skipped and `finish_reason!=success`, the run returns **failure**.
   - If `--force-unsuccessful` is set, failed outputs are **not** skipped.

2. **Prepare environment**
   - Output directory is (re)created.
   - Agent config is copied to output.
   - If `--reuse-successful-plan` is set (or `--force` is not set):
     - Plan artifacts are preserved when `--plan` is used.
     - Multiplan artifacts are preserved when `--multiplan` is used.
   - Podman client is initialized.

3. **Plan (optional, `--plan`)**
   - Generates `/output/refactoring_plan.md`.
   - On success, `inference_metadata.json` is renamed to `plan_metadata.json`.
   - Description type in metadata is suffixed with `_plan`.

4. **Multiplan (optional, `--multiplan`)**
   - Generates `/output/refactoring_plans/refactoring_plan0..4.md`.
   - On success, `inference_metadata.json` is renamed to `multiplan_generation_metadata.json`.
   - Judge selects a plan and writes `multiplan_metadata.json`.
   - Description type in metadata is suffixed with `_multiplan`.

5. **Inference (always)**
   - Uses plan content if `--plan` or `--multiplan` was used.
   - Runs the agent in the runtime container.
   - Produces `prediction.diff` and `inference_metadata.json`.
   - Description type in metadata is suffixed with `_plan` or `_multiplan` when applicable.

## Outputs
- `prediction.diff`: git diff of changes.
- `inference_metadata.json`: agent metadata (finish_reason, cost, description_type).
- Plan mode:
  - `refactoring_plan.md`
  - `plan_metadata.json`
- Multiplan mode:
  - `refactoring_plans/refactoring_plan0..4.md`
  - `multiplan_generation_metadata.json`
  - `multiplan_metadata.json`
  - `judge.out`

## Finish reasons
- `success`: run completed.
- `timeout`: inference timed out.
- `error_planmode`: plan timed out or invalid.
- `error_multiplan`: multiplan timed out or invalid.
- `error_judge`: judge failed.

## Description type suffixes
- Standard inference: `description_type`
- Plan inference: `description_type_plan`
- Multiplan inference: `description_type_multiplan`

These suffixes also apply to timeout/fallback metadata.
