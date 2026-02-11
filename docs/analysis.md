# Analysis Phase

The analysis phase aggregates evaluation results across agents and description types and generates plots.

## Entry point
```bash
python -m refactoring_benchmark.scripts.analyze
```

## What it does
1. **Discover output directories** (defaults to all `output*` folders).
2. **Load evaluation results** and attach inference metadata when available.
3. **Filter** by agent ID, description type, or success status.
4. **Compute metrics** (IFR, test success, precision, cost, etc.).
5. **Generate plots** and optional summary tables.

## Common usage
```bash
# Default plots (IFR + test success)
python -m refactoring_benchmark.scripts.analyze

# Compare two agents
python -m refactoring_benchmark.scripts.analyze --agent-id agentA --agent-id agentB

# Only successful inference runs
python -m refactoring_benchmark.scripts.analyze --successful-only

# Precision metrics (requires pseudo agents)
python -m refactoring_benchmark.scripts.analyze --metric precision_overall
```

## Outputs
- Plots saved to `./analyze/` (configurable via `--plots-dir`).
- Optional statistics table (`--statistics`).

## Precision metrics
Precision metrics require evaluated **pseudo agents** (`golden_agent` and `null_agent`).
Use:
```bash
python -m refactoring_benchmark.tools.create_pseudo_agents --agent golden --agent null
python -m refactoring_benchmark.scripts.evaluate --agent-id golden_agent
python -m refactoring_benchmark.scripts.evaluate --agent-id null_agent
```
