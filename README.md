# 🧑‍🍳 CodeTaste

[![Paper](https://img.shields.io/badge/Paper-arXiv:XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX) 
[![Website](https://img.shields.io/badge/Website-CodeTaste-blue)](https://codetaste.logicstar.ai/)

CodeTaste is a benchmark for evaluating AI agents on real-world code refactoring tasks and measuring their alignment with human developer choices. It builds per‑instance execution environments, runs agents in locked‑down containers, evaluates their performance with tests and static analysis rules, and aggregates results into plots and tables.

---

## 🚀 Core Concepts

* **Instance**: A specific repo + commit pair combined with rules ($\Gamma$) and descriptions.
* **Track (Description Type)**: The level of detail provided to the agent. Reflected as `description-type` in the CLI.
    * *Instructed Track:* Detailed blueprints specifying exact transformations.
    * *Open Track:* High-level focus areas where the agent must recover human architectural choices.
* **Mode**: The agent's execution strategy (`direct`, `plan`, or `multiplan`).

---

## 📊 Metrics Explained

CodeTaste evaluates agents strictly on functional correctness and adherence to refactoring intent.

* **Functional Correctness ($\text{Pass}$):** Ensures the predicted patch ($\hat{X}$) does not degrade the test suite beyond empirical bounds established by $k=5$ runs on the original and golden codebases:
  $$\text{Pass}(\hat{X}) = \mathbb{1} \Big[ F_{\hat{X}} \leq \max_i \{F_R^{(i)}, F^{*,(i)}\} \land P_{\hat{X}} \geq \min_i \{P_R^{(i)}, P^{*,(i)}\} \Big]$$
  In practice, bounds are computed from baseline runs of the `null_agent` and `golden_agent` pseudo-agents.
* **Instruction Following Rate ($\text{IFR}$):** Measures recall of additive ($\Gamma^+$) and reductive ($\Gamma^-$) static analysis rules:
  $$\text{IFR}(\Gamma, \hat{X}) = \frac{|\Gamma^-|}{|\Gamma|} \text{IFR}^-(\Gamma, \hat{X}) + \frac{|\Gamma^+|}{|\Gamma|} \text{IFR}^+(\Gamma, \hat{X})$$
* **Alignment Score ($\mathcal{A}$):** Reported as `ifr_x_test_success` in analysis. It only rewards instruction adherence when tests are valid:
  $$\mathcal{A}(\Gamma, \hat{X}) = \text{pass}(\hat{X}) \times \text{IFR}(\Gamma, \hat{X})$$
* **Change Precision ($\text{Prec}$):** Measures the extent to which a patch avoids unrelated changes outside the scope of the rule set. Requires evaluated pseudo-agents (see below).

**Pseudo-agents:** The benchmark uses two special agents to compute baselines and precision:
* **`null_agent`** represents the base commit $R$.
* **`golden_agent`** represents the golden commit $R \circ X^{*}$.
These are materialized as pseudo-agent outputs so they can be evaluated by the same pipeline as real agents.

---

## 🛠 Prerequisites & Hardware

* **Python:** >= 3.10 (managed via [Poetry](https://python-poetry.org/) >= 2.0.0).
* **Containerization:** [Podman](https://podman.io/) (for secure, isolated execution).
* **Hardware:** Execution scripts use multi-processing by default (configurable workers). Ensure sufficient RAM/CPU.
* **Utilities:** `unzip` (for `codetaste100.zip`) and `zip` (for combining split `outputs.zip` parts).
* **API Keys:**
    * **Anthropic:** Set via `ANTHROPIC_API_KEY`. Required by default for the setup agent (`bootstrap`) and the judge (`multiplan` inference). *Note: Can be overridden by editing the judge/setup source files.*
    * **Your Agent's Key:** Set via `API_KEY_PASSED_TO_AGENT` for inference.

### Podman Setup (Required)
Ensure the user socket is enabled so the Python client can communicate with the daemon:
```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### Image Registry Override (Optional)
By default, images are pulled from `ghcr.io/logic-star-ai/codetaste`. Override with:
```bash
export CODETASTE_IMAGE_REPOSITORY=ghcr.io/logic-star-ai/codetaste
```

---

## 📥 Quickstart

```bash
# 0. Deactivate any existing virtual environment to enable in-project .venv creation
# 1. Install dependencies
poetry install && source .venv/bin/activate

# 2. Download benchmark artifacts (assets, instance_images, metadata, pseudo-agents)
curl -L -o codetaste100.zip "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip"
unzip -o codetaste100.zip -d . && rm codetaste100.zip

# 3. Pull the base container image
podman pull ghcr.io/logic-star-ai/codetaste/benchmark-base-all:latest
```

---

## 🔄 The Pipeline

### 1. Inference (Generating Patches)

Run your agent against the benchmark. Results are cached by default in `outputs/`.

```bash
chmod +x ./entrypoint.sh # Required for runtime images

python -m refactoring_benchmark.cli.inference \
  --instances 10 \
  --agent-dir ./agents/your-agent \
  --description-type instructed \
  --output-dir ./outputs/instructed/direct \
  --env API_KEY_PASSED_TO_AGENT="$API_KEY_PASSED_TO_AGENT"
  # Optional: append --plan or --multiplan
```

**Handling Inference Errors:** If you choose to rerun inference from scratch, note that we perform a full restart of an instance run if an agent fails due to unexpected API errors or if it incorrectly places plans in `plan`/`multiplan` modes. However, runs that hit the monetary budget limit (e.g., $11 per task) are evaluated using whatever output is available.

### 2. Evaluation (Testing & IFR)

Applies the generated `prediction.diff`, calculates static analysis rules, and runs the test suite up to 5x to account for flakiness.

```bash
python -m refactoring_benchmark.cli.evaluate \
  --instances 10 \
  --agent-id <your-agent-id> \
  --output-dir ./outputs/instructed/direct
```

### 3. Analysis (Visualizing Results)

Generate the plots and tables used in the CodeTaste paper.

```bash
# Generate all plots
chmod +x run_analyze.sh
./run_analyze.sh
```

---

## 📈 Reproducing the Paper's Results

To reproduce the exact plots and tables found in the CodeTaste paper without rerunning the expensive inference pipeline, you can use our precomputed outputs.

1. **Download Precomputed Outputs:**
Run the included script to download and extract the evaluation data into the `outputs/` directory, or rerun inference and evaluation from scratch for all instances, agents, description types and modes.

```bash
chmod +x download_outputs.sh
./download_outputs.sh
```


2. **Generate Plots and Tables:**
Instantly regenerate all analytical charts.
```bash
./run_analyze.sh
```

---

## 📂 Output Directory Structure

```text
outputs/
└── <description_type>/   # instructed | open
    └── <mode>/           # direct | plan | multiplan
        └── <owner>/<repo>/<hash8>/<agent_id>/
            ├── prediction.diff           # The generated patch
            ├── inference_metadata.json   # Cost, finish reasons, etc.
            └── evaluation/
                ├── evaluation_result.json
                ├── rules_positive.sarif  # IFR+ data
                ├── rules_negative.sarif  # IFR- data
                ├── test_output.txt       # Raw test logs
                └── rule_output.txt       # Raw rule logs
```

---

## 📖 Documentation

For detailed guides on specific phases of the pipeline, refer to our documentation:

* [`docs/bootstrap.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/bootstrap.md) - Building per-instance runtime images.
* [`docs/inference.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/inference.md) - Running agents to generate patches.
* [`docs/evaluation.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/evaluation.md) - Applying patches, running tests, and computing IFR.
* [`docs/analysis.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/analysis.md) - Aggregating metrics and generating plots.
* [`docs/benchmarking-your-agent.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/benchmarking-your-agent.md) - Guide to testing your own custom agent.
