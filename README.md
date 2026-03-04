<div align="center">
  <img src="https://codetaste.logicstar.ai/static/images/codetaste_logo.svg" width="250" alt="CodeTaste Logo">
  <h1>CodeTaste</h1>
  <a href="https://arxiv.org/abs/XXXX.XXXXX">
    <img src="https://img.shields.io/badge/Paper-arXiv:XXXX.XXXXX-b31b1b.svg" alt="Paper Badge">
  </a>
  <a href="https://codetaste.logicstar.ai/">
    <img src="https://img.shields.io/badge/Website-CodeTaste-blue.svg" alt="Website Badge">
  </a>
  <!-- License MIT -->
  <a href="https://opensource.org/license/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License Badge">
  </a>
</div>

## 📖 Overview

CodeTaste is a benchmark for evaluating AI agents on real-world code refactoring tasks and measuring their alignment with human developer choices. It builds per‑instance execution environments, runs agents in locked‑down containers, evaluates their performance with tests and static analysis rules.

> Check out our Paper for more details: [CodeTaste: Can LLMs Generate Human-Level Code Refactorings?](https://arxiv.org/abs/XXXX.XXXXX).

---

## 🚀 Setup

### 🛠 Prerequisites & Hardware

* **Python:** >= 3.10 (managed via [Poetry](https://python-poetry.org/) >= 2.0.0).
* **Containerization:** [Podman](https://podman.io/) (for secure and reproducible executions).
* **Hardware:** Execution scripts multiple parralel containers by default (configurable workers). Ensure that you have sufficient RAM, CPU and storage. We recommend running the evaluation and inference harness on a `x86_64` machine having 16 CPU cores and 32GB of RAM per parallel worker. You should have at least 500GB of free disk space to accommodate the base images, instance-specific runtime images, and outputs.
* **Utilities:** `unzip` (for `codetaste100.zip`) and `zip` (for combining split `outputs.zip` parts).
* **API Keys:**
    * **Anthropic:** Set via `ANTHROPIC_API_KEY`. Required by default for the agent used for environment creation (`bootstrap`) and the judge (`multiplan` inference). *Note: Can be overridden by editing the judge/bootstrap source files.*
    * **Your Agent's Key:** Set via `API_KEY_PASSED_TO_AGENT` for inference.

#### Podman Setup (Required)
Ensure the user socket is enabled so the Python client can communicate with the daemon:
```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

#### Image Registry Override (Optional)
By default, images are pulled from `ghcr.io/logic-star-ai/codetaste`. Override with:
```bash
export CODETASTE_IMAGE_REPOSITORY=ghcr.io/logic-star-ai/codetaste
```

### 💽 Installation

```bash
# 0. Deactivate any existing virtual environment to enable in-project .venv creation
# 1. Install dependencies
git clone git@github.com:logic-star-ai/codetaste.git && cd codetaste
poetry install && source .venv/bin/activate

# 2. Download benchmark artifacts (assets, instance_images, metadata, pseudo-agents)
curl -L -o codetaste100.zip "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/codetaste100.zip"
unzip -o codetaste100.zip -d . && rm codetaste100.zip

# 3. Pull the base container image
podman pull ghcr.io/logic-star-ai/codetaste/benchmark-base-all:latest

# 4. Verify that you can run tests
pytest
```

---

## 🔄 The Pipeline

### 1. Inference (Generating Patches)

Run your agent against the benchmark. Results are outputted and cached by default in `outputs/`.

```bash
chmod +x ./entrypoint.sh # Required for runtime images

python -m refactoring_benchmark.cli.inference \
  --instances 100 \
  --agent-dir ./agents/your-agent \
  --description-type instructed \
  --output-dir ./outputs/instructed/direct \
  --env API_KEY_PASSED_TO_AGENT="$API_KEY_PASSED_TO_AGENT"
  # Optional: append --plan or --multiplan
```

**Handling Inference Errors:** We do a full restart of the inference for an instance (i.e. deletion of the corresponding instance output directory `outputs/<description_type>/<mode>/<owner>/<repo>/<hash>/<agent_id>/` and rerunning inference) if either (1) the agent doesn't produce results, due to an unexpected error (e.g. LLM Provider cannot be reached) or (2) the agent fails to place plan(s) under the expected path.

### 2. Evaluation (Testing & IFR)

Applies the generated `prediction.diff`, calculates static analysis rules, and runs the test suite up to 5x to account for flakiness.

```bash
python -m refactoring_benchmark.cli.evaluate \
  --instances 100 \
  --agent-id <your-agent-id> \
  --output-dir ./outputs/instructed/direct
```

**Adjust and run `run_agent_description.sh`** to run both inference and evaluation in one go.

#### 📂 Output Directory Structure

After this step. the `outputs/` directory will be populated with the results of the inference and evaluation.

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

### 3. Analysis (Visualizing Results)

Generate the plots and tables used in the CodeTaste paper.

```bash
chmod +x run_analyze.sh
./run_analyze.sh
```

The metrics come in 4 main categories: (1) Pass: Checks whether the model's patch preserves functional integrity, using the repository's test suite. (2) IFR: Measures whether the patch follows the intended refactoring using static analysis checks. (3) Alignment:  A combined score that only rewards rule compliance when tests are valid, and (4) Change Precision: Measures how well the patch avoids unrelated changes outside the intended refactoring scope. The golden commit reference solutions achieve 57.5%.

### Submitting Results to the leaderboard

We list top performing agentic systems on our [leaderboard](https://codetaste.logicstar.ai/). If you want your results included, please share a brief description of your approach, the corresponding `outputs/` (with traces) and `plots/` directories, and a link to the project's homepage. Please contact us at [alex@logicstar.ai](mailto:alex@logicstar.ai) for submissions.
If you want independent verification of the results, we also require the `agent/` directory containing the exact agent implementation used for inference.

> The inclusion in the leaderboard will be performed on a best effort basis, but we can not guarantee inclusion or timely processing of your requests.

---

### 📈 Reproducing the Paper's Results

To reproduce the exact plots and tables found in the CodeTaste paper without rerunning the inference pipeline, you can use our precomputed outputs.

1. **Download Precomputed Outputs:**
Run the included script to download and extract the evaluation data into the `outputs/` directory, or download the `outputs.{zip,z01,z02,z03}` from our [Github Releases](https://github.com/logic-star-ai/codetaste/releases) and extract them manually.

```bash
chmod +x download_outputs.sh
./download_outputs.sh
```

2. **Generate Plots and Tables:**
Regenerate all analytical charts.
```bash
chmod +x run_analyze.sh
./run_analyze.sh
```

---

## 📖 Additional Documentation

For detailed guides on specific phases of the pipeline, refer to our documentation:

* [`docs/bootstrap.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/bootstrap.md) - Building runtime images.
* [`docs/inference.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/inference.md) - Running agents to generate patches.
* [`docs/evaluation.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/evaluation.md) - Applying patches, running tests, and computing IFR.
* [`docs/analysis.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/analysis.md) - Aggregating metrics and generating plots.
* [`docs/benchmarking-your-agent.md`](https://github.com/logic-star-ai/codetaste/blob/main/docs/benchmarking-your-agent.md) - Guide to testing your own custom agent.

---

## 💫 Contributions

We would love to hear from the broader NLP, Machine Learning, and Software Engineering research communities, and welcome contributions to CodeTaste! If you have suggestions for improvements, new features, or want to report issues, please open an issue or submit a pull request on our GitHub repository.

---

## ✍️ Citation

```
@article{codetaste2026,
  title={CodeTaste: Can LLMs Generate Human-Level Code Refactorings?},
  author={Alex Thillen and Niels Mündler and Veselin Raychev and Martin Vechev},
  year={2026},
  eprint={TBD},
  archivePrefix={arXiv}
}
```

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.