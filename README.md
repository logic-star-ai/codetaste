

## Usage

### Bootstrap Benchmark Instances

```bash
python -m refactoring_benchmark.scripts.bootstrap --help
```

```
usage: bootstrap.py [-h] [--instances INSTANCES] [--instances-csv INSTANCES_CSV] [--nr-workers NR_WORKERS] [--force-runtime-build] [--rerun-metrics] [--force-full-build]

Bootstrap benchmark instances

options:
  -h, --help            show this help message and exit
  --instances INSTANCES
                        Number of instances to bootstrap (default: 10)
  --instances-csv INSTANCES_CSV
                        Path to instances CSV file (default: ./instances.csv)
  --nr-workers NR_WORKERS
                        Number of parallel workers (default: 4)
  --force-runtime-build
                        Force rebuild of runtime images even if they exist (reuses setup image and metadata)
  --rerun-metrics       Rerun metrics collection on existing setup images (cheap, reuses agent setup)
  --force-full-build    Force full rebuild from scratch: setup + runtime (expensive, reruns agent)
```

### Inference Phase

```bash
python -m refactoring_benchmark.scripts.inference --help
```

```
Run inference on benchmark instances using agent scripts.

options:
  -h, --help            show this help message and exit
  --instances INSTANCES
                        Number of instances to run from the CSV file (default: 15)
  --instances-csv INSTANCES_CSV
                        Path to the instances CSV file (default: instances.csv)
  --nr-workers NR_WORKERS
                        Number of parallel workers (threads) for inference (default: 4)
  --agent-dir AGENT_DIR
                        Path to the agent directory containing setup_system.sh, run_agent, and agent_config.json (default: agent)
  --output-dir OUTPUT_DIR
                        Base directory for inference outputs (default: None)
  --timeout TIMEOUT     Timeout in seconds for each instance inference (default: 3600)
  --force               Force re-run inference even if outputs already exist (default: False)
  --env KEY=VALUE       Environment variable to pass to containers (can be specified multiple times) (default: [])
  --description-type {standard,minimal,open,nano}
                        Type of task description to use (standard: full description, minimal: title and summary only, open: open-ended refactoring prompt, nano: very brief description) (default: standard)
```

### Evaluation Phase

```bash
python -m refactoring_benchmark.scripts.evaluate --help
```

```
usage: evaluate.py [-h] [--instances INSTANCES] [--instances-csv INSTANCES_CSV] --agent-id AGENT_ID [--nr-workers NR_WORKERS] [--output-dir OUTPUT_DIR] [--timeout-test TIMEOUT_TEST] [--timeout-rule TIMEOUT_RULE] [--force]

Evaluate inference results using test and rule-based metrics.

options:
  -h, --help            show this help message and exit
  --instances INSTANCES
                        Number of instances to run from the CSV file (default: 15)
  --instances-csv INSTANCES_CSV
                        Path to the instances CSV file (default: instances.csv)
  --agent-id AGENT_ID   Agent ID to evaluate (must match directory name in output) (default: None)
  --nr-workers NR_WORKERS
                        Number of parallel workers (threads) for evaluation (default: 4)
  --output-dir OUTPUT_DIR
                        Base directory for inference outputs (default: output)
  --timeout-test TIMEOUT_TEST
                        Timeout in seconds for test evaluation (default: 20 minutes) (default: 1200)
  --timeout-rule TIMEOUT_RULE
                        Timeout in seconds for rule evaluation (default: 20 minutes) (default: 1200)
  --force               Force re-evaluation even if results already exist (default: False)
```

### Analyze Phase

To compute and plot precision, the following `output_pseudo_agents/` directory must exist and must contain the pseudo-agents `null_agent` and `golden_agent` and it must have been evaluated as we need the sarif files.

```bash
python -m refactoring_benchmark.scripts.analyze --help
```
