# Refactoring Benchmark

A benchmarking framework for evaluating AI agents on real-world code refactoring tasks. It builds per‑instance execution environments, runs agents in locked‑down containers, evaluates outputs with tests + static rules, and aggregates results into plots and tables.

## What this repo provides
- **Bootstrap**: Build per‑instance Podman images and collect baseline test metrics.
- **Inference**: Run agents to generate patches (`prediction.diff`) with optional planning modes.
- **Evaluation**: Apply patches, run tests, and compute rule‑based metrics (IFR).
- **Analysis**: Aggregate results across agents/description types and generate plots.

## Requirements
- **Python** (see `pyproject.toml`) with Poetry.
- **Podman** for container execution.
- **opengrep** for rule evaluation inside containers.
- **Anthropic API key** for bootstrap setup agent and multiplan judge (if used).

## Quickstart
```bash
poetry install
export ANTHROPIC_API_KEY=...  # required for bootstrap and multiplan judge
```

### 1) Bootstrap instances
```bash
python -m refactoring_benchmark.scripts.bootstrap \
  --instances 10 \
  --instances-csv ./instances.csv
```

### 2) Run inference
```bash
python -m refactoring_benchmark.scripts.inference \
  --instances 10 \
  --agent-dir ./agents/your-agent \
  --description-type instructed
```

### 3) Evaluate outputs
```bash
python -m refactoring_benchmark.scripts.evaluate \
  --instances 10 \
  --agent-id your-agent-id
```

### 4) Analyze
```bash
python -m refactoring_benchmark.scripts.analyze --metric ifr --plot-type line
```

## Project layout
```
refactoring_benchmark/
  bootstrap/        # Phase 1: container image setup
  inference/        # Phase 2: agent execution
  evaluation/       # Phase 3: tests + rule evaluation
  analyze/          # Phase 4: analysis and plotting
  podman/           # Podman helpers
  utils/            # Shared models + helpers
  tools/            # Utilities for pseudo agents, descriptions, analysis
assets/             # Rules, descriptions, diffs
instance_images/    # Per-instance bootstrap artifacts
entrypoint.sh       # Container entrypoint for inference/evaluation
instances.csv       # Benchmark instance definitions
```

## Core concepts
- **Instance**: A specific repo + commit pair with rules and descriptions.
- **Prediction**: Agent output stored as `prediction.diff`.
- **IFR (Instruction Following Rate)**: How well rules are followed.
- **Description types**: Task detail level (`instructed` or `open`). Both can be used in direct, plan, or multiplan modes.

## Tools & scripts
- **Bootstrap**: `python -m refactoring_benchmark.scripts.bootstrap`
- **Inference**: `python -m refactoring_benchmark.scripts.inference`
- **Evaluation**: `python -m refactoring_benchmark.scripts.evaluate`
- **Analysis**: `python -m refactoring_benchmark.scripts.analyze`
- **Pseudo agents**: `python -m refactoring_benchmark.tools.create_pseudo_agents`

## Outputs (per instance + agent)
```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/
  prediction.diff
  inference_metadata.json
  evaluation/
    evaluation_result.json
    rules_positive.sarif
    rules_negative.sarif
    test_output.txt
```

## Migration (breaking change)
To move legacy `output*` folders into the new layout and rewrite metadata:
```bash
python -m refactoring_benchmark.tools.migrate_outputs
```

## Documentation
Detailed phase docs:
- `docs/bootstrap.md`
- `docs/inference.md`
- `docs/evaluation.md`
- `docs/analysis.md`

## Notes for public release
- The benchmark uses **Podman** (not Docker) by default.
- `entrypoint.sh` supports `inference`, `plan`, `multiplan`, `eval_test`, `eval_rule`.
- Some workflows assume `assets/` and `instance_images/` are populated.
