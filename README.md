# Refactoring Benchmark

A secure, isolated benchmark system for evaluating AI agents on real-world code refactoring tasks.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue)](https://python-poetry.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

## Overview

This benchmark evaluates AI agents on their ability to perform code refactoring tasks by:

1. **Isolating the agent** in a secure container environment
2. **Preventing cheating** through network isolation and git sanitization
3. **Evaluating results** via test suites and static analysis rules

The system ensures that agents cannot access the "golden" (correct) refactoring or fetch solutions from external sources.

## Key Features

- 🔒 **Security Isolation**: Network blocking, privilege separation, git sanitization
- 📊 **Multi-Mode Evaluation**: Test-based and rule-based assessment
- 🐳 **Containerized**: Each benchmark instance runs in a reproducible Docker container
- 🎯 **Real-World Tasks**: Based on actual refactoring commits from major open-source projects
- 📈 **Automated Setup**: Claude agent bootstraps environment and validates tests
- 🔍 **Hidden Rules**: Static analysis rules remain invisible to the agent during inference

## Quick Start

```bash
# 1. Install dependencies
poetry install --with dev

# 2. Set API key
export ANTHROPIC_API_KEY=your_key_here

# 3. Build base images
cd refactoring_benchmark/base_images/
docker build -t benchmark-base-python -f Dockerfile.python .

# 4. Bootstrap instances
cd ../..
poetry run python -m refactoring_benchmark.scripts.bootstrap

# 5. Run inference
mkdir -p agent output
echo '#!/bin/bash\ncd /testbed\n# Your agent logic' > agent/run_agent
chmod +x agent/run_agent

docker run --rm \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $(pwd)/agent:/agent \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    inference

# 6. Evaluate
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_test
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   BOOTSTRAP PHASE                            │
│                                                               │
│  Clone Repo → Setup Env → Verify Tests → Inject Security   │
│   (buggy)     (Claude)     (buggy/golden)   (rules/router)  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    RUNTIME PHASE                             │
│                                                               │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐ │
│  │  Inference  │ →  │  Eval: Tests │ →  │  Eval: Rules   │ │
│  │  (isolated) │    │    (JSON)    │    │    (SARIF)     │ │
│  └─────────────┘    └──────────────┘    └────────────────┘ │
│   - Blocked net      - Apply patch       - Apply patch     │
│   - No sudo          - Run tests         - Run Semgrep     │
│   - Read tasks       - JSON output       - SARIF output    │
│   - No rules access                                         │
└─────────────────────────────────────────────────────────────┘
```

## Runtime Modes

### 1. Inference Mode
Agent refactors code with security restrictions:
- GitHub domains sinkholed (cannot fetch solutions)
- Golden commit physically removed from git history
- Runs as unprivileged `agent_user`
- Can read task descriptions
- Cannot access evaluation rules

### 2. Test Evaluation Mode
Validates correctness:
- Applies the agent's patch
- Runs the test suite
- Outputs JSON results (passed/failed/total)

### 3. Rule Evaluation Mode
Assesses code quality:
- Applies the agent's patch
- Runs Semgrep/Opengrep with hidden rules
- Outputs SARIF format results
- Checks for anti-patterns removed and good patterns added

## Project Structure

```
refactoring-benchmark/
├── refactoring_benchmark/       # Main package
│   ├── base_images/             # Base container Dockerfiles
│   ├── scripts/
│   │   └── bootstrap.py         # Build benchmark instances
│   └── utils/                   # Shared utilities
├── rules/                       # Static analysis rules (HIDDEN)
│   └── {owner}/{repo}/{hash}/
│       ├── rules_positive.yml   # Good patterns to find
│       └── rules_negative.yml   # Anti-patterns to avoid
├── descriptions/                # Task descriptions (VISIBLE)
│   └── {owner}/{repo}/{hash}/
│       └── README.md            # Task explanation for agent
├── instance_images/             # Saved container artifacts
│   └── {repo}/{owner}/{hash}/
│       └── scripts/             # Setup scripts
├── tests/                       # Test suite (31 tests, 100% coverage)
├── logs/                        # Bootstrap and instance logs
├── instances.csv                # Benchmark instance definitions
├── entrypoint.sh                # Container runtime router
├── pyproject.toml               # Python dependencies
├── CLAUDE.md                    # Setup guide
└── RUNTIME.md                   # Runtime execution guide
```

## Benchmark Instances

Current instances (from `instances.csv`):

| Repository | Category | Language | Buggy Commit | Golden Commit |
|------------|----------|----------|--------------|---------------|
| ray-project/ray | structural | python | f781622f | e4ceae19 |
| tensorflow/tensorflow | structural | python | 56bbd227 | 98a2d7d1 |
| pandas-dev/pandas | api | python | 8b56ea30 | f39a9ce5 |
| apache/airflow | structural | python | c14d2ea0 | 773f52fe |
| autokey/autokey | structural | python | 9309c4fe | 85b948e7 |

## Security Model

The benchmark implements multiple layers of security:

### Network Isolation
```bash
# GitHub domains redirected to localhost
127.0.0.1 github.com
127.0.0.1 api.github.com
127.0.0.1 raw.githubusercontent.com
```

### Git Sanitization
1. Remove remote origin
2. Expire all reflogs
3. Prune unreachable objects (golden commit)
4. Aggressive garbage collection

### Privilege Separation
| User | Permissions | Purpose |
|------|-------------|---------|
| `benchmarker` | sudo access | Bootstrap setup |
| `agent_user` | no sudo | Run agent (inference) |
| `root` | full access | Evaluation modes only |

### File Permissions
| Directory | Owner | Mode | Agent Access |
|-----------|-------|------|--------------|
| `/rules/` | root:root | 700 | ❌ Denied |
| `/task_description/` | agent_user | 755 | ✅ Allowed |
| `/testbed/` | agent_user | 755 | ✅ Allowed |

## Example: Adding a New Instance

### 1. Add to instances.csv
```csv
owner,repo,commit_hash,golden_commit_hash,combined_score,category,language
django,django,abc123...,def456...,0.75,structural,python
```

### 2. Create evaluation rules
```bash
mkdir -p rules/django/django/abc123ab
# Add rules_positive.yml and rules_negative.yml
```

### 3. Create task description
```bash
mkdir -p descriptions/django/django/abc123ab
# Add README.md describing the refactoring task
```

### 4. Bootstrap
```bash
poetry run python -m refactoring_benchmark.scripts.bootstrap
```

The system will:
- Clone the repository
- Run Claude to set up the environment
- Verify tests pass at both buggy and golden commits
- Save setup scripts if quality criteria met
- Inject security components
- Commit the benchmark container

## Development

### Running Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=refactoring_benchmark --cov-report=html

# Specific test class
poetry run pytest tests/test_bootstrap.py::TestGoldenMetricsCriteria
```

### Code Quality
```bash
# Format code
poetry run black refactoring_benchmark/

# Type checking (if added)
poetry run mypy refactoring_benchmark/
```

### Debugging
```bash
# View bootstrap logs
tail -f logs/bootstrap.log

# View instance-specific logs
tail -f logs/bootstrap-owner-repo-hash.log

# Inspect container
docker run -it benchmark-base-python bash
```

## Evaluation Metrics

### Test-Based Metrics
- **Passed**: Number of tests that pass
- **Failed**: Number of tests that fail
- **Total**: Total number of tests
- **Pass Rate**: `passed / total`

### Rule-Based Metrics
- **Negative Rules**: Anti-patterns that should be removed
- **Positive Rules**: Good patterns that should be added
- **SARIF Output**: Detailed rule violations and locations

### Quality Criteria
Scripts are saved from containers when:
- **Total tests** ≥ 10
- **Pass rate** ≥ 30%

## Documentation

- **[CLAUDE.md](CLAUDE.md)**: Complete setup guide
- **[RUNTIME.md](RUNTIME.md)**: Runtime execution details
- **[rules/README.md](rules/README.md)**: Rule creation guide
- **[descriptions/README.md](descriptions/README.md)**: Task description templates
- **[tests/README.md](tests/README.md)**: Testing documentation

## Requirements

- Python 3.12+
- Poetry for dependency management
- Docker or Podman
- Anthropic API key (for bootstrap phase)

## Troubleshooting

### Docker Connection Failed
```bash
# For Podman users
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### Bootstrap Failures
1. Check `logs/bootstrap.log` for errors
2. Ensure base images are built
3. Verify API key is set
4. Review instance-specific logs

### Container Issues
```bash
# List all benchmark containers
docker images | grep localhost/benchmark

# Remove all benchmark images
docker images | grep localhost/benchmark | awk '{print $3}' | xargs docker rmi -f

# Clean up
docker system prune -f
```

## Contributing

1. Add new benchmark instances via `instances.csv`
2. Create corresponding rules and descriptions
3. Run bootstrap to validate
4. Add tests for new functionality
5. Update documentation

## License

See LICENSE file for details.

## Acknowledgments

- Built with [Claude](https://claude.ai) for environment setup
- Uses [Semgrep](https://semgrep.dev) for static analysis
- Inspired by real-world refactoring challenges from major open-source projects

## Citation

If you use this benchmark in your research, please cite:

```bibtex
@software{refactoring_benchmark,
  title = {Refactoring Benchmark: A Secure Evaluation System for AI Code Refactoring},
  author = {Author Name},
  year = {2025},
  url = {https://github.com/username/refactoring-benchmark}
}
```
