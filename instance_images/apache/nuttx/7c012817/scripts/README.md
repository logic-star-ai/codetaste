# Apache NuttX Test Scripts

This directory contains scripts for setting up and running tests on the Apache NuttX RTOS codebase.

## Scripts

### `/scripts/setup_system.sh`
System-level setup script that runs with `sudo` privileges. For NuttX, this script is a no-op as no system services are required for basic testing.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### `/scripts/setup_shell.sh`
Shell environment setup script that configures the testing environment. This script:
- Creates a Python virtual environment
- Installs code quality tools (black, flake8, codespell, etc.)
- Builds the nxstyle code checker
- Sets up PATH and environment variables

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**Note:** Must be sourced (not executed) to properly set environment variables in the current shell.

### `/scripts/run_tests`
Test execution script that runs a representative suite of code quality and validation tests.

**Usage:**
```bash
/scripts/run_tests
```

**Output:** Produces JSON output in the format:
```json
{"passed": N, "failed": M, "skipped": K, "total": T}
```

## Complete Test Run

To run the complete test suite from a clean state:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Test Categories

The test suite includes:
1. **Code Style Tests**: Validates C code using nxstyle
2. **Python Linting**: Checks Python code with black and flake8
3. **Spell Checking**: Validates documentation with codespell
4. **Repository Structure**: Ensures critical files and directories exist
5. **Git Repository**: Validates repository integrity
6. **C Compilation**: Smoke tests for compiler functionality

## Requirements

- Ubuntu 24.04 or compatible Linux distribution
- Python 3.8 or later
- GCC compiler
- Git

## Notes

- Scripts are idempotent and safe to run multiple times
- Works on both HEAD and HEAD~1 commits
- Does not modify versioned files in `/testbed/`
- All build artifacts are stored in `${HOME}/.nuttx-tools`

For detailed information, see [SUMMARY.md](SUMMARY.md).
