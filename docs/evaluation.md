# ✅ Evaluation Phase

The evaluation phase applies an agent’s patch, runs tests, and executes rule checks to compute IFR.

## Entry point
```bash
python -m refactoring_benchmark.cli.evaluate
```

## What it does
1. **Locate outputs** for each instance + agent.
2. **Test evaluation** (`refactoring_benchmark/bootstrap/entrypoint.sh eval_test`)
   - Apply `prediction.diff`.
   - Run the instance’s test script.
   - Parse test results from container output.
3. **Rule evaluation** (`refactoring_benchmark/bootstrap/entrypoint.sh eval_rule`)
   - Apply `prediction.diff`.
   - Run opengrep with positive and negative rules.
   - Produce SARIF and YAML outputs.
4. **Persist results** in `evaluation/evaluation_result.json`.

## Prerequisites
- `outputs/<description_type>/<mode>/...` from inference.
- `instance_images/<owner>/<repo>/<hash>/instance_metadata.json` (from `codetaste100.zip` or bootstrap).
- Rule files under `assets/rules/<owner>/<repo>/<hash>/` by default. Use `--rules-dir` to evaluate with an alternate root such as `assets/rules-curated`.

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
- `--rules-dir`: root directory containing per-instance `rules_positive.yml` and `rules_negative.yml`.
- `--timeout-test`: test run timeout in seconds.
- `--timeout-rule`: rule run timeout in seconds.
- `--force`: re-run evaluation even if results already exist.
- `--retry-null-tests`: re-run only if test metrics are missing.
- `--skip-tests`: run rule evaluation only.

## Metrics
- **Test metrics**: pass/fail/skip counts and pass rate.
- **Rule metrics**: matched positive/negative rules and IFR.
- **EvaluationResult**: combines instance metadata, agent config, inference metadata, and metrics.
