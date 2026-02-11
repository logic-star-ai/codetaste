# Evaluation Phase

The evaluation phase applies an agent’s patch, runs tests, and executes rule checks to compute IFR.

## Entry point
```bash
python -m refactoring_benchmark.scripts.evaluate
```

## What it does
1. **Locate outputs** for each instance + agent.
2. **Test evaluation** (`entrypoint.sh eval_test`)
   - Apply `prediction.diff`.
   - Run the instance’s test script.
   - Parse test results from container output.
3. **Rule evaluation** (`entrypoint.sh eval_rule`)
   - Apply `prediction.diff`.
   - Run opengrep with positive and negative rules.
   - Produce SARIF and YAML outputs.
4. **Persist results** in `evaluation/evaluation_result.json`.

## Outputs
```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/evaluation/
  evaluation_result.json
  rules_positive.sarif
  rules_negative.sarif
  test_output.txt
  rule_output.txt
```

## Key flags
- `--agent-id`: which agent directory to evaluate (required).
- `--timeout-test`: test run timeout in seconds.
- `--timeout-rule`: rule run timeout in seconds.
- `--force`: re-run evaluation even if results already exist.
- `--retry-null-tests`: re-run only if test metrics are missing.
- `--skip-tests`: run rule evaluation only.

## Metrics
- **Test metrics**: pass/fail/skip counts and pass rate.
- **Rule metrics**: matched positive/negative rules and IFR.
- **EvaluationResult**: combines instance metadata, agent config, inference metadata, and metrics.
