# TensorFlow Testing Scripts

## Overview

This directory contains scripts to setup and run TensorFlow tests in a reproducible manner.

## Scripts

### `/scripts/setup_system.sh`
System-level setup executed with sudo privileges. Currently minimal as no system services are required.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### `/scripts/setup_shell.sh`
Configures the shell environment for TensorFlow development and testing. Must be sourced to set environment variables.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**What it does:**
- Sets up Python 3.11 environment
- Configures GCC 11 compiler
- Installs Python dependencies (numpy, absl, six, wrapt, protobuf)
- Configures TensorFlow build via configure.py
- Sets required environment variables

### `/scripts/run_tests`
Executes the test suite and outputs results in JSON format.

**Usage:**
```bash
/scripts/run_tests
```

**Output:** Single JSON line to stdout:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Complete Workflow

To run tests from a clean state:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Requirements

- **Bazel 3.7.2**: Installed in `/usr/local/bin`
- **GCC 11/G++ 11**: Installed via system package manager
- **Python 3.11**: Installed via uv
- **System packages**: python3-dev, python3-numpy

## Notes

- Scripts are idempotent and safe to run multiple times
- Scripts work on both HEAD and HEAD~1 commits
- Git working tree remains clean after execution
- All build artifacts are in ignored directories (.tf_configure.bazelrc, bazel-*)
