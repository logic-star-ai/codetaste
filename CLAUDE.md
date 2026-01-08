# Refactoring Benchmark

A comprehensive benchmarking framework for evaluating AI agents' code refactoring capabilities. Tests agents on real-world refactoring tasks and measures their instruction-following rate (IFR) through test execution and static analysis.

## Overview

The benchmark evaluates how well AI agents can:
- Follow specific refactoring instructions (positive rules: patterns to implement)
- Avoid anti-patterns (negative rules: bad patterns to avoid)
- Maintain test suite validity
- Generate correct code patches

## Architecture

The system operates in four main phases:

### 1. Bootstrap Phase (`refactoring_benchmark/bootstrap/`)
Sets up containerized execution environments for each benchmark instance.

**Process:**
1. **Setup Phase**: Creates base execution environment using AI agent assistance
2. **Runtime Phase**: Installs dependencies, runs baseline tests, captures metrics
3. **Output**: Two Podman images per instance (`setup_image`, `runtime_image`) + baseline metrics

**Entry point:** `refactoring_benchmark/scripts/bootstrap.py`

### 2. Inference Phase (`refactoring_benchmark/inference/`)
Runs AI agents on benchmark instances to generate refactoring patches.

**Process:**
1. Loads agent configuration from `agent/agent_config.json`
2. Executes agent in isolated container (`runtime_image`)
3. Extracts git diff as `prediction.diff`
4. Saves inference metadata

**Entry point:** `refactoring_benchmark/scripts/inference.py`

### 3. Evaluation Phase (`refactoring_benchmark/evaluation/`)
Evaluates agent outputs through parallel test execution and static analysis.

**Process (parallel):**
- **Test Evaluation**: Applies patch, runs test suite, calculates pass rate
- **Rule Evaluation**: Applies patch, runs opengrep SARIF rules, calculates IFR

**Metrics:**
- `TestMetrics`: passed/failed/skipped counts, pass_rate, validity
- `RuleMetrics`: positive/negative rule matches, IFR scores
- `EvaluationResult`: Combined test + rule metrics

**Entry point:** `refactoring_benchmark/scripts/evaluate.py`

### 4. Analysis Phase (`refactoring_benchmark/analyze/`)
Aggregates results, computes statistics, generates visualizations.

**Features:**
- Load all evaluation results from output directory
- Filter by agent, instance, validity status
- Calculate aggregate IFR metrics
- Generate comparison plots

**Entry point:** `refactoring_benchmark/scripts/analyze.py`

## Key Components

### Data Models (Pydantic)
- `InstanceRow` (`utils/models.py`): Benchmark instance from CSV
- `AgentConfig` (`inference/models.py`): Agent metadata
- `EvaluationResult` (`evaluation/models.py`): Complete evaluation data
- Coverage models (`coverage/models.py`): Code coverage data structures

### Container Management (`podman/`)
- Uses Podman (not Docker) for container orchestration
- Automatic cleanup on exit/errors
- Isolated execution with network blocking

### Orchestrators
- `BootstrapOrchestrator`: Parallel bootstrap execution
- `InferenceOrchestrator`: Parallel agent runs
- `EvaluationOrchestrator`: Parallel evaluation with test + rule workers

All use `ThreadPoolExecutor` with graceful shutdown handling.

## Project Structure

```
refactoring_benchmark/
├── bootstrap/          # Phase 1: Environment setup
├── inference/          # Phase 2: Agent execution
├── evaluation/         # Phase 3: Results evaluation
├── analyze/            # Phase 4: Analysis & visualization
├── podman/             # Container management utilities
├── coverage/           # Code coverage parsing
├── utils/              # Shared utilities, models, prompts
├── tools/              # Utilities (pseudo agents, description builder)
├── scripts/            # Main entry points
└── base_images/        # Docker base image definitions

instances.csv           # Benchmark instance definitions
entrypoint.sh          # Container entry point (3 modes)
pyproject.toml         # Poetry project configuration
```

## Key Files

- **`instances.csv`**: Benchmark definitions (owner, repo, commits, category, language)
- **`entrypoint.sh`**: Container entry point supporting modes: `inference`, `eval_test`, `eval_rule`

## Metrics

### Instruction Following Rate (IFR)
- **Positive IFR**: Fraction of good patterns successfully implemented
- **Negative IFR**: Fraction of bad patterns successfully avoided
- **Total IFR**: Combined score across all rules

### Test Validity
Tests are considered valid if:
- No crashes during execution
- At least 10 tests run
- Fewer than 10,000 tests run

### Evaluation Result
Each instance produces:
- Test metrics (pass/fail/skip counts, pass_rate)
- Rule metrics (positive/negative matches, IFR scores)
- Validity flags for filtering analysis

## Technologies

- **Python 3.x** with Poetry dependency management
- **Podman >=5.6.0** for container orchestration
- **Pydantic >=2.0.0** for data validation
- **Pandas** for data analysis
- **Matplotlib** for visualizations
- **PyYAML** for configuration
- **Pytest** for testing

## Workflows

### Running Bootstrap
```bash
python -m refactoring_benchmark.scripts.bootstrap
```

### Running Inference
```bash
python -m refactoring_benchmark.scripts.inference
```

### Running Evaluation
```bash
python -m refactoring_benchmark.scripts.evaluate
```

### Running Analysis
```bash
python -m refactoring_benchmark.scripts.analyze
```

### Creating Pseudo Agent Outputs
Create baseline comparison agents without running actual inference:

```bash
python -m refactoring_benchmark.tools.create_pseudo_agents --agent golden --agent null --output-dir output_minimal
```

Both agents create complete output structures (prediction.diff, agent_config.json, inference_metadata.json) compatible with evaluation.

## Output Structure

```
output/
└── {instance_id}/
    └── {agent_name}/
        ├── prediction.diff           # Generated patch
        ├── inference_metadata.json   # Inference details
        ├── evaluation_result.json    # Evaluation metrics
        └── logs/                      # Execution logs
```

## Development

### Contributing
Special care should be taken to write clean, lean and maintainable code. It's important to explore the repository enough to avoid code duplication! 

### Testing
```bash
pytest                           # Run all tests
pytest -m unit                   # Unit tests only
pytest -m integration            # Integration tests
pytest --cov                     # With coverage report
```

### Code Formatting
```bash
black ./refactoring_benchmark
```

## Container Modes

The `entrypoint.sh` supports three execution modes:

1. **inference**: Runs agent, captures git diff
2. **eval_test**: Applies patch, runs tests
3. **eval_rule**: Applies patch, runs static analysis (opengrep)

All modes include security hardening (network sinkholing, restricted user execution).
