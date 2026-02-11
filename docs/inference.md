# Inference Phase

This document summarizes how inference runs for a single instance.

## Entry point
```bash
python -m refactoring_benchmark.scripts.inference
```

## Phases
1. **Skip check**
   - If `prediction.diff` exists and `--force` is not set, the instance is skipped.
   - If `--force-unsuccessful` is set, only successful runs are skipped.

2. **Prepare environment**
   - Output directory is (re)created.
   - `agent_config.json` is copied into the output folder.
   - Existing plan artifacts are preserved when `--reuse-successful-plan` is set.

3. **Plan (optional, `--plan`)**
   - Agent generates `/output/refactoring_plan.md`.
   - On success, `inference_metadata.json` is renamed to `plan_metadata.json`.

4. **Multiplan (optional, `--multiplan`)**
   - Agent generates `/output/refactoring_plans/refactoring_plan0..4.md`.
   - A judge selects the best plan and writes `multiplan_metadata.json`.
   - On success, `inference_metadata.json` is renamed to `multiplan_generation_metadata.json`.

5. **Inference (always)**
   - Runs the agent inside the runtime container.
   - Produces `prediction.diff` and `inference_metadata.json`.
   - Description type is suffixed with `_plan` or `_multiplan` when applicable.

## Outputs
- `prediction.diff`: git diff of the agent’s changes.
- `inference_metadata.json`: finish reason, cost, description type, timestamps.
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
- Direct inference: `description_type`
- Plan inference: `description_type_plan`
- Multiplan inference: `description_type_multiplan`

## Description types
- `instructed`: full task description.
- `open`: higher‑level abstract description (can be used in normal, plan, or multiplan modes).
