# Refactoring Benchmark - Setup Guide

A benchmark system for evaluating AI agents on code refactoring tasks with security isolation and multi-mode evaluation.

## Prerequisites

- **Python**: 3.12+
- **Poetry**: For dependency management
- **Docker/Podman**: For containerization
- **Anthropic API Key**: For Claude agent during bootstrap

```bash
# Set Docker socket for Podman users
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

## Quick Start

### 1. Install Dependencies

```bash
# Install project dependencies
poetry install --with dev

# Activate virtual environment
poetry shell
```

### 2. Configure API Key

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Build Base Images

```bash
# Build base images for each language
cd refactoring_benchmark/base_images/
docker build -t benchmark-base-python -f Dockerfile.python .
```

### 4. Bootstrap Instances

```bash
# Build benchmark instances from instances.csv
poetry run python -m refactoring_benchmark.scripts.bootstrap
```

This will:
- **Phase 1 (Setup)**: Clone repo, run Claude agent, verify tests, commit setup image
- **Phase 2 (Runtime)**: Inject runtime components and security rules, commit runtime image
- Creates two images per instance: `{owner}__{repo}-{hash}__setup` and `{owner}__{repo}-{hash}__runtime`

### 5. Run Inference

```bash
# Create agent script
mkdir -p agent
cat > agent/run_agent << 'EOF'
#!/bin/bash
cd /testbed
# Your refactoring logic
EOF
chmod +x agent/run_agent

# Run inference
mkdir -p output
docker run --rm \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $(pwd)/agent:/agent \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    inference
```

### 6. Evaluate Results

```bash
# Test evaluation
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_test

# Rule evaluation
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_rule
```

## Project Structure

```
refactoring-benchmark/
├── refactoring_benchmark/
│   ├── base_images/           # Dockerfiles for base images
│   ├── scripts/
│   │   └── bootstrap.py       # Build benchmark containers
│   └── utils/
│       ├── container_utils.py # Docker container utilities
│       ├── logger.py          # Logging infrastructure
│       ├── models.py          # Pydantic data models
│       └── prompts.py         # Agent setup prompts
├── assets/                    # Benchmark assets
│   ├── rules/                 # Static analysis rules (hidden from agent)
│   │   └── {owner}/{repo}/{hash}/
│   │       ├── rules_positive.yml
│   │       └── rules_negative.yml
│   └── descriptions/          # Task descriptions (visible to agent)
│       └── {owner}/{repo}/{hash}/
│           └── README.md
├── instance_images/           # Saved scripts from containers
│   └── {repo}/{owner}/{hash}/
│       └── scripts/
├── tests/                     # Pytest test suite
├── logs/                      # Bootstrap logs
├── instances.csv              # Benchmark instances
├── entrypoint.sh              # Container runtime router
└── pyproject.toml             # Dependencies
```

## Key Concepts

### Three Runtime Modes

1. **Inference**: Agent refactors code with security restrictions
   - Network blocked (GitHub sinkholed)
   - Git history sanitized (golden commit removed)
   - Runs as unprivileged `agent_user`
   - Can read task descriptions, cannot access rules

2. **Test Evaluation**: Applies patch and runs test suite
   - Validates correctness
   - Outputs JSON test results

3. **Rule Evaluation**: Applies patch and runs static analysis
   - Uses Semgrep/Opengrep rules
   - Outputs SARIF format results
   - Rules hidden from agent during inference

### Security Model

| Component | Visibility | Permissions | Purpose |
|-----------|-----------|-------------|---------|
| `/rules/` | Hidden | root:root 700 | Evaluation criteria |
| `/task_description/` | Visible | agent_user 755 | Task guidance |
| `/testbed/` | Visible | agent_user 755 | Code to refactor |

## Common Commands

```bash
# Run tests
poetry run pytest

# Run specific test
poetry run pytest tests/test_bootstrap.py::TestGoldenMetricsCriteria

# Check coverage
poetry run pytest --cov=refactoring_benchmark --cov-report=html

# Format code
poetry run black refactoring_benchmark/

# View logs
tail -f logs/bootstrap.log
tail -f logs/bootstrap-{owner}-{repo}-{hash}.log

# List containers
docker ps -a

# Remove all benchmark images
docker images | grep localhost/benchmark | awk '{print $3}' | xargs docker rmi -f
```

## Adding New Instances

### 1. Add to instances.csv

```csv
owner,repo,commit_hash,golden_commit_hash,combined_score,category,language
owner,repo,buggy_hash,golden_hash,0.7,structural,python
```

### 2. Create Rules

```bash
mkdir -p assets/rules/{owner}/{repo}/{hash[:8]}
# Create rules_positive.yml and rules_negative.yml
```

### 3. Create Task Description

```bash
mkdir -p assets/descriptions/{owner}/{repo}/{hash[:8]}
# Create README.md with task description
```

### 4. Bootstrap

```bash
poetry run python -m refactoring_benchmark.scripts.bootstrap
```

## Development Workflow

### 1. Testing Changes

```bash
# Run tests after code changes
poetry run pytest -v

# Check specific functionality
poetry run pytest tests/test_bootstrap.py -k "save_criteria"
```

### 2. Debugging Bootstrap

```bash
# Check logs for specific instance
tail -f logs/bootstrap-owner-repo-hash.log

# Manually inspect container
docker run -it benchmark-base-python bash
```

### 3. Iterating on Rules

```bash
# Test rules locally
semgrep --config assets/rules/{owner}/{repo}/{hash}/rules_negative.yml /path/to/code
```

## Troubleshooting

### Docker Connection Failed
```bash
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
docker ps  # Verify connection
```

### Bootstrap Fails
- Check logs in `logs/` directory
- Ensure base images are built
- Verify API key is set
- Check instances.csv format

### Tests Don't Pass in Container
- Review golden vs buggy commit diffs
- Check if tests are flaky
- Verify environment setup in logs

### Agent Cannot Access Files
- Task descriptions should be in `assets/descriptions/` (visible)
- Rules should be in `assets/rules/` (hidden)
- Check entrypoint.sh permissions logic

## Next Steps

- **RUNTIME.md**: Detailed runtime execution guide
- **assets/rules/README.md**: Rule creation guidelines
- **assets/descriptions/README.md**: Task description templates
- **tests/README.md**: Testing documentation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Bootstrap Phase 1: Setup                 │
│  ┌────────────┐  ┌──────────┐  ┌─────────┐  ┌───────────┐ │
│  │ Clone Repo │→ │Setup Env │→ │ Verify  │→ │  Commit   │ │
│  │ (golden)   │  │ (Claude) │  │ Tests   │  │{id}__setup│ │
│  └────────────┘  └──────────┘  └─────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Bootstrap Phase 2: Runtime                  │
│  ┌────────────┐  ┌──────────┐  ┌─────────┐  ┌───────────┐ │
│  │   Inject   │→ │  Inject  │→ │ Inject  │→ │  Commit   │ │
│  │ Entrypoint │  │  Rules   │  │  Tasks  │  │{id}__rtme │ │
│  └────────────┘  └──────────┘  └─────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     Runtime Execution                        │
│  ┌────────────┐  ┌──────────┐  ┌─────────────────────────┐ │
│  │ Inference  │→ │eval_test │→ │    eval_rule (SARIF)    │ │
│  │ (isolated) │  │  (JSON)  │  │   (Semgrep/Opengrep)    │ │
│  └────────────┘  └──────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## License

See LICENSE file for details.
