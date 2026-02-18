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
- **Anthropic API key** only if you run bootstrap (setup agent) and/or multiplan (judge).
- `unzip` to extract the released benchmark artifacts (`codetaste100.zip`).
- `assets/` and `instance_images/` are populated for the instances in `instances.csv`.

## Quickstart
```bash
# deactivate any activated virtual environment

poetry install # or /path/to/venv/with/poetry install ; this will create an in-project virtualenv

# This repo uses an in-project virtualenv (see poetry.toml)
source .venv/bin/activate

# Download benchmark artifacts (assets/, instance_images/, plots/, outputs/pseudo_agents/)
curl -L -o codetaste100.zip "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip"
unzip -o codetaste100.zip -d .
rm codetaste100.zip

# Optional: download precomputed inference/evaluation outputs (outputs/)
curl -L -O "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/outputs.zip.a{a,b,c,d}"
cat outputs.zip.a* > outputs.zip
unzip -o outputs.zip -d .
rm outputs.zip outputs.zip.a*
```

## Podman setup (required)
The benchmark uses the Podman API via the Python `podman` client. In a typical rootless setup you need the user socket enabled and `DOCKER_HOST` pointing at it:
```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### 1) Bootstrap instances
Bootstrap builds per-instance runtime images and writes instance metadata. **This step is only required if you want to build runtime images yourself, instead of using the provided runtime images.**
```bash
export ANTHROPIC_API_KEY=...  # required for bootstrap setup agent
python -m refactoring_benchmark.cli.bootstrap \
  --instances 10 \
  --instances-csv ./instances.csv
```

### 2) Run inference
Make sure that you have `assets/` and `instance_images/` in your project directory.
```bash
python -m refactoring_benchmark.cli.inference \
  --instances 10 \
  --agent-dir ./agents/your-agent \
  --description-type instructed \
  --output-dir ./outputs/instructed/direct \
  --env API_KEY_PASSED_TO_AGENT="$API_KEY_PASSED_TO_AGENT"
  # add one of the following for different modes:
  # --plan, --multiplan (by default it runs in direct mode)
```

*Note:* By default inference results are cached, i.e. if `prediction.diff` and `inference_metadata.json` exist in the corresponding `./outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/` directory, inference is skipped. You can use `--force` to rerun inference unconditionally. `--force-unsuccessful` forces rerun, whenever the agent doesn't report `finish_reason=success`.

### 3) Evaluate outputs
`--agent-id` must match the `id` in your agent's `agent_config.json` (it is used as the output directory name created during inference).
```bash
python -m refactoring_benchmark.cli.evaluate \
  --instances 10 \
  --agent-id <agent-id-from-agent_config.json> \
  --output-dir ./outputs/instructed/direct # adjust
```

**Note: You can use `run_agent_description.sh` to run inference and evaluation with automatically setup of the output directories for a given description type and mode.**

### 4) Analyze
```bash
python -m refactoring_benchmark.cli.analyze --metric ifr --plot-type bar
```

#### Generate all plots + tables
```bash
./run_analyze.sh
```

### E2E pipeline
Runs inference + evaluation across instructed/open and direct/plan/multiplan for a small slice, then generates plots.
```bash
python -m refactoring_benchmark.cli.e2e_smoke \
  --instances 2 \
  --agent-dir ./agents/qwen-code/qwen3-coder-30b-a3b-instruct
```

## Reproducing results
Two paths:
1) Use released benchmark artifacts + existing runtime images (recommended when available).
2) Build runtime images yourself via bootstrap (slower; non-deterministic).

### Path A: Use released artifacts (recommended)
The `codetaste100.zip` release artifact contains `assets/`, `instance_images/`. Extract it into the repo root:
```bash
curl -L -o codetaste100.zip https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip
unzip -o codetaste100.zip -d .
```

*Note:* If you downloaded `outputs.zip`, you can regenerate plots immediately:
```bash
./run_analyze.sh
```

To run inference/evaluation yourself you need the Podman runtime images locally (`localhost/benchmark/<id>__runtime`).

### Path B: Build runtime images locally (bootstrap)
Prerequisites (must exist):
1. `instances.csv`
2. `assets/` (rules, descriptions, diffs)
The following are generated by bootstrap and required for inference/evaluation:
3. `instance_images/<owner>/<repo>/<hash>/instance_metadata.json` for each instance (created by bootstrap)
4. Podman runtime images: `localhost/benchmark/<id>__runtime` (created by bootstrap)

```bash
export ANTHROPIC_API_KEY=...  # required for bootstrap setup agent
python -m refactoring_benchmark.cli.bootstrap \
  --instances 100 \
  --instances-csv ./instances.csv
```

### Steps (run-to-run comparable)
1. Use the provided instance set (default: `instances.csv`) and keep it consistent across all steps (`--instances 100`).
2. Run inference for each agent and mode (direct/plan/multiplan) over the same instance set. 
Example:
```bash
python -m refactoring_benchmark.cli.inference \
  --instances 100 \
  --agent-dir ./agents/<agent>/<model> \
  --description-type instructed \
  --output-dir ./outputs/<track>/<mode> \
  --env API_KEY_PASSED_TO_AGENT="$API_KEY_PASSED_TO_AGENT"
  # add one: --plan or --multiplan (omit both for direct)
  # output-dir options : ./outputs/<instructed|open>/<direct|plan|multiplan>
```
3. Run evaluation for the corresponding outputs. Example:
```bash
python -m refactoring_benchmark.cli.evaluate \
  --instances 100 \
  --agent-id <agent-id> \
  --output-dir ./outputs/<track>/<mode>
```
*Note:* Explore the `--help` section to explore features, such as only re-evaluating based on rules.

4. Regenerate plots and tables (requires evaluated `outputs/...` from steps 2-4):
```bash
./run_analyze.sh
# or: python -m refactoring_benchmark.cli.analyze
```

This rebuilds `outputs/<description_type>/<mode>/...` and refreshes `plots/`.

### Notes

#### Handling inference errors

For our results, we do a full restart of the inference (i.e. deletion of the corresponding instance output directory `outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/` and rerunning inference) if one of the following events occurs:
- Agent doesn't produce results, due to an unexpected error (e.g. LLM Provider cannot be reached).
- Agent fails to place plans in the right place in plan and multiplan modes.

Both cases happen relatively rarely, even for small models, like Qwen3-30B. We find them by investigating `inference.out` of unsuccessful runs.

Further, we re-evaluate instances that don't produce test results in the first evaluation up to 4x. This is to account for non-determinism in the test execution. E.g. a test result could rely on an external API being accessible.

#### Practical tips

You can fill in the variable names in `run_agent_description.sh` to run **inference** + **evaluation** for a given (description type, mode, agent) combination across the whole instance set.

## Project layout
```
refactoring_benchmark/
  bootstrap/        # Phase 1: container image setup
  inference/        # Phase 2: agent execution
  evaluation/       # Phase 3: tests + rule evaluation
  analyze/          # Phase 4: analysis and plotting
  podman/           # Podman helpers
  utils/            # Shared models + helpers
assets/             # Rules, descriptions, diffs (codetaste100.zip)
instance_images/    # Per-instance bootstrap artifacts (codetaste100.zip)
instances.csv       # Benchmark instance definitions (codetaste100.zip)
```

## Core concepts
- **Instance**: A specific repo + commit pair with rules and descriptions.
- **Prediction**: Agent patch stored as `prediction.diff`.
- **IFR (Instruction Following Rate)**: What fraction of the rules (instructions) were followed by the agent, measured via static analysis of the predicted patch.
- **Description types (aka Track)**: Task detail level (`instructed` or `open`). Both can be used in direct, plan, or multiplan modes. **For our analysis, we only use planning modes for the open track.**
- **Modes**: Execution strategy (`direct`, `plan`, or `multiplan`), tracked separately from description type.

## Tools & CLI
- **Bootstrap**: `python -m refactoring_benchmark.cli.bootstrap`
- **Inference**: `python -m refactoring_benchmark.cli.inference`
- **Evaluation**: `python -m refactoring_benchmark.cli.evaluate`
- **Analysis**: `python -m refactoring_benchmark.cli.analyze`
- **Golden and Null agents**: `python -m refactoring_benchmark.cli.create_pseudo_agents`

## Outputs (per instance + agent)
```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/
  prediction.diff # the patch
  inference_metadata.json # contains data from the inference, such as finish_reason, cost, ...
  evaluation/
    evaluation_result.json
    rules_positive.sarif
    rules_negative.sarif
    test_output.txt
```

## Documentation
Detailed phase docs:
- `docs/bootstrap.md`
- `docs/inference.md`
- `docs/evaluation.md`
- `docs/analysis.md`
- `docs/benchmarking-your-agent.md`
