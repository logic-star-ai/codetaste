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
podman build -t benchmark-base-python -f Dockerfile.python .
podman build -t benchmark-base-javascript -f Dockerfile.javascript .

# 4. Bootstrap instances
cd ../..
poetry run python -m refactoring_benchmark.scripts.bootstrap

# 5. Run inference
mkdir -p agent output
echo '#!/bin/bash\ncd /testbed\n# Your agent logic' > agent/run_agent
chmod +x agent/run_agent

# 6. Execute benchmark container
...

# 7. Evaluate results
...
```
