# Analysis Phase

The analysis phase aggregates evaluation results across agents and description types and generates plots.

## Entry point
```bash
python -m refactoring_benchmark.cli.analyze
```

## Output layout
Results are expected under:
```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/
```

## What it does
1. **Discover output directories** (defaults to all `outputs/<description_type>/<mode>` directories).
2. **Load evaluation results** and attach inference metadata when available.
3. **Filter** by agent ID, description type, mode, or success status.
4. **Compute metrics** (IFR, test success, precision, cost, etc.).
5. **Generate plots** and optional summary tables.

## Common usage
```bash
# Default plots (IFR + test success)
python -m refactoring_benchmark.cli.analyze

# Compare two agents
python -m refactoring_benchmark.cli.analyze --agent-id agentA --agent-id agentB

# Only successful inference runs
python -m refactoring_benchmark.cli.analyze --successful-only

# Filter by mode
python -m refactoring_benchmark.cli.analyze --mode direct --mode plan

# Precision metrics (requires pseudo agents)
python -m refactoring_benchmark.cli.analyze --metric precision_overall
```

## Outputs
- Plots saved to `./analyze/` (configurable via `--plots-dir`).
- Optional statistics table (`--statistics`).

## Precision metrics
Precision metrics require evaluated **pseudo agents** (`golden_agent` and `null_agent`).
Use:
```bash
python -m refactoring_benchmark.tools.create_pseudo_agents --agent golden --agent null
python -m refactoring_benchmark.cli.evaluate --agent-id golden_agent --output-dir outputs/pseudo_agents/direct
python -m refactoring_benchmark.cli.evaluate --agent-id null_agent --output-dir outputs/pseudo_agents/direct
```
