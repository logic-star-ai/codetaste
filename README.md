# CodeTaste

CodeTaste is a benchmark for evaluating AI agents on real-world code refactoring tasks and measure their alignment with human developer choices. It builds per‑instance execution environments, runs agents in locked‑down containers, evaluates their performance with tests and static analysis rules, and aggregates results into plots and tables.

## Core concepts
- **Instance**: A specific repo + commit pair with rules and descriptions.
- **Prediction**: Agent patch stored as `prediction.diff`.
- **IFR (Instruction Following Rate)**: What fraction of the rules (instructions) were followed by the agent, measured via static analysis of the predicted patch.
- **Description types (aka Track)**: Task detail level (`instructed` or `open`). Both can be used in direct, plan, or multiplan modes. **For our analysis, we only use planning modes in the open tracks.**
- **Modes**: Execution strategy (`direct`, `plan`, or `multiplan`), tracked separately from description type.

## Outputs (per instance + agent)
```
outputs/<description_type>/<mode>/<owner>/<repo>/<hash8>/<agent_id>/
  prediction.diff # the patch
  inference_metadata.json # contains data from the inference, such as finish_reason, cost, ...
  evaluation/
    evaluation_result.json
    rules_positive.sarif
    rules_negative.sarif
    test_output.txt
```

## Baseline results
Baseline test runs are stored under `baseline_results/<owner>/<repo>/<hash8>/` as JSONL files (one run per line) and are used to validate pass results. For reproducibility, regenerate baselines on your platform to account for environment-specific discrepancies.
Populate baselines with:
```bash
python -m refactoring_benchmark.cli.baseline_results --runs 5 --instances 100
```

## What this repo provides
- **Bootstrap**: Build per‑instance Podman images and collect baseline test metrics.
- **Inference**: Run agents to generate patches (`prediction.diff`) with optional planning modes.
- **Evaluation**: Apply patches, run tests, and compute rule‑based metrics (IFR).
- **Analysis**: Aggregate results across agents, tracks and modes and generate plots.

## Requirements
- **Python** (see `pyproject.toml`) with Poetry (`>=2.0.0`).
- **Podman** for container execution.
- **Anthropic API key** only if you run bootstrap (setup agent) and/or multiplan (judge).
- `unzip` to extract the released benchmark artifacts (`codetaste100.zip`).
- `assets/` and `instance_images/` are populated for the instances in `instances.csv`. `instance_images/` is automatically populated if you run bootstrap.

## Quickstart
```bash
# deactivate any activated virtual environment, so a new one is created in the project by Poetry

poetry install # poetry version >=2.0.0

# This repo uses an in-project virtualenv (see poetry.toml)
source .venv/bin/activate

# Download benchmark artifacts (assets/, instance_images/, outputs/pseudo_agents/direct/)
curl -L -o codetaste100.zip "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip"
unzip -o codetaste100.zip -d .
rm codetaste100.zip

# Optional: download precomputed inference/evaluation outputs (outputs/)
curl -fL -O "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/outputs.zip"
# Download split parts if present (outputs.z01, outputs.z02, ...).
for i in $(seq -w 1 99); do
  part="outputs.z${i}"
  url="https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/${part}"
  if ! curl -fL -o "${part}" "${url}"; then
    rm -f "${part}"
    break
  fi
done
zip -s 0 outputs.zip --out combined.zip
unzip -o combined.zip -d .
rm -f outputs.zip outputs.z* combined.zip

chmod +x ./entrypoint.sh
```

## Podman setup (required)
The benchmark uses the Podman API via the Python `podman-py` client. In a typical rootless setup you need the user socket enabled and `DOCKER_HOST` pointing at it:
```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### Image registry config
Image names default to `ghcr.io/logic-star-ai/codetaste/...`. Override with:
```bash
export CODETASTE_IMAGE_REPOSITORY=ghcr.io/logic-star-ai/codetaste
```

### 1) Bootstrap instances (optional)
Bootstrap builds per-instance runtime images and writes instance metadata. 
**This step is only required if you want to build setup & runtime images yourself, instead of using the provided images.**
**Make sure to pull the base image `ghcr.io/logic-star-ai/codetaste/benchmark-base-all:latest` to speed up bootstrap. (or run `podman build -t ghcr.io/logic-star-ai/codetaste/benchmark-base-all:latest -f refactoring_benchmark/base_images/Dockerfile.all .` in the repo root)**
```bash
export ANTHROPIC_API_KEY=...  # required for bootstrap setup agent
python -m refactoring_benchmark.cli.bootstrap \
  --instances 10 \
  --instances-csv ./instances.csv
```

### 2) Run inference
Make sure that you have `assets/` and `instance_images/` in your project directory.
```bash
chmod +x ./entrypoint.sh # mounted into the runtime images for inference

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
  --output-dir ./outputs/instructed/direct # adjust track and mode
```

**Note: You can use `run_agent_description.sh` to run inference and evaluation with automatic setup of the output directories for a given description type and mode.**

### 4) Analyze
```bash
python -m refactoring_benchmark.cli.analyze --metric ifr --plot-type bar
```

#### Generate all plots + tables for the paper
```bash
chmod +x run_analyze.sh
./run_analyze.sh
```

### E2E pipeline
Runs inference + evaluation across instructed/open and direct/plan/multiplan for a small slice of instances, then generates plots.
```bash
python -m refactoring_benchmark.cli.e2e_smoke \
  --instances 2 \
  --agent-dir ./agents/your-agent
```

## Reproducing results
Two paths:
1) Use released benchmark artifacts + existing runtime images (recommended).
2) Build runtime images yourself via bootstrap (slower; non guaranteed to lead to the same images)

### Path A: Use released artifacts (recommended)
The `codetaste100.zip` release artifact contains `assets/`, `instance_images/` and `outputs/pseudo_agents/direct` (for the instances in `instances.csv`). Extract it into the repo root:
```bash
curl -L -o codetaste100.zip https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip
unzip -o codetaste100.zip -d .
```

*Note:* If you downloaded `outputs.zip`, you can regenerate plots immediately:
```bash
chmod +x run_analyze.sh
./run_analyze.sh
```

To run inference/evaluation yourself you need the Podman runtime images locally (`ghcr.io/logic-star-ai/codetaste/<id>__runtime`). Images are auto-pulled if missing.

### Path B: Build runtime images locally (bootstrap)
Prerequisites (must exist):
1. `instances.csv`
2. `assets/` (rules, descriptions, diffs)
The following are generated by bootstrap and required for inference/evaluation:
3. `instance_images/<owner>/<repo>/<hash>/instance_metadata.json` for each instance (created by bootstrap)
4. Have pulled the base image: `podman pull ghcr.io/logic-star-ai/codetaste/benchmark-base-all`

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

For the published results, we do a full restart of the inference (i.e. deletion of the corresponding instance output directory `outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/` and rerunning inference) if one of the following events occurs:
- Agent doesn't produce results, due to an unexpected error (e.g. LLM Provider cannot be reached).
- Agent fails to place plans in the right place in plan and multiplan modes.

Both cases happen relatively rarely, even for small models, like `qwen3-coder-30b-a3b-instruct`. We find them by investigating `inference.out` of unsuccessful runs. If a model hits budget constraints or time limit, we don't consider it an error and include the results in the analysis.

Further, we re-evaluate instances that don't produce test results in the first evaluation up to 4x. This is to account for the non-determinism we observed in build processes, test executions and parsing, when using `/scripts` generated in **bootstrap** phase.

#### Practical tips

You can fill in the variable names in `run_agent_description.sh` to run **inference** + **evaluation** for a given tuple (description type, mode, agent) combination across the whole instance set.

## Documentation
Detailed phase docs:
- `docs/bootstrap.md`
- `docs/inference.md`
- `docs/evaluation.md`
- `docs/analysis.md`
- `docs/benchmarking-your-agent.md`
