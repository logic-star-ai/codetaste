# Benchmarking Your Own Agent

This guide focuses on what you (the user) need to provide to add an agent and run it in the benchmark.

## What you must provide
Create a new agent directory under `agents/<agent-name>/<model-name>/` with these files:

```
agents/your-agent/your-model/
  agent_config.json   # required
  run_agent           # required (executable)
  setup_system.sh     # optional
```

### agent_config.json (required)
This file is validated by `refactoring_benchmark.inference.validation.validate_agent_config`.
Required fields:

```
{
  "id": "your-agent-id",
  "agent": {
    "name": "your-agent-name",
    "version": "1.0.0",
    "provider": "local",
    "additional": {}
  },
  "model": {
    "name": "your-model-name",
    "provider": "local",
    "additional": {}
  }
}
```

### run_agent (required)
Your script runs inside a locked-down container as `agent_user`. It must:
- Read the task prompt from `/task_description/description.md`.
- Modify the repo mounted at `/testbed`.
- Write `/output/inference_metadata.json` with at least:
  - `finish_reason` (one of: `success`, `timeout`, `execution_error`, `error`, `unknown`, `budget_exceeded`, `error_planmode`, `error_multiplan`, `error_judge`)
  - Optional: `cost_usd`, `start_time`, `finish_time`, `additional`
- Exit non-zero if the run fails.

You do NOT need to write `prediction.diff`. The entrypoint will run `git add -A` and write `/output/prediction.diff` after your script finishes.

### Plan / Multiplan outputs (prompt already instructs)
If you run `--plan` or `--multiplan`, the framework prepends prompts that instruct the agent to create the plan files.
Your agent just needs to follow the prompt and write the files:

Plan mode (`--plan`):
- `/output/refactoring_plan.md`

Multiplan mode (`--multiplan`):
- `/output/refactoring_plans/refactoring_plan0.md`
- `/output/refactoring_plans/refactoring_plan1.md`
- `/output/refactoring_plans/refactoring_plan2.md`
- `/output/refactoring_plans/refactoring_plan3.md`
- `/output/refactoring_plans/refactoring_plan4.md`

## Optional: setup_system.sh
If present, `setup_system.sh` runs before network access is blocked. Use it to install system dependencies (CLI tools, language runtimes, etc.) that your agent needs.

## Running the pipeline

Run inference:
```bash
python -m refactoring_benchmark.cli.inference \
  --instances 10 \
  --agent-dir ./agents/your-agent/your-model \
  --description-type instructed
  # --plan
  # --multiplan
  # --env API_KEY=...
```

Evaluate:
```
python -m refactoring_benchmark.cli.evaluate \
  --instances 10 \
  --agent-id your-agent-id \
  --output-dir ./outputs/instructed/direct  # change to ./outputs/<description_type>/<mode> if needed
```

## Evaluation outputs and layout
Evaluation writes under the agent output directory:

```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/evaluation/
  evaluation_result.json
  rules_positive.sarif
  rules_negative.sarif
  test_output.txt
  rule_output.txt
```

The parent output directory (created by inference) also includes:

```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/
  prediction.diff
  inference_metadata.json
  evaluation/
    ...
```
