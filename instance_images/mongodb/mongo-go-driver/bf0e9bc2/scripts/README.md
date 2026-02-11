# MongoDB Go Driver Test Scripts

This directory contains scripts for setting up and running tests for the MongoDB Go Driver project.

## Scripts Overview

### setup_system.sh
System-level configuration script that must be executed with `sudo`. For this project, no system services are required, so it simply exits successfully.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### setup_shell.sh
Shell environment setup script that configures the environment for running tests. This script:
- Verifies Go is installed
- Downloads Go module dependencies
- Sets required environment variables

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**Note:** This script must be sourced (not executed) to properly set environment variables.

### run_tests
Executes the test suite and outputs results in JSON format. This script:
- Runs Go tests with the `-short` flag to skip integration tests
- Parses test results using Python
- Outputs a JSON line with test counts

**Usage:**
```bash
/scripts/run_tests
```

**Output Format:**
```json
{"passed": 7143, "failed": 0, "skipped": 70, "total": 7213}
```

## Complete Test Execution

To run the full test pipeline:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Requirements

- Go 1.23.4+ (pre-installed in the environment)
- Python 3 (for JSON parsing)
- No external services required (unit tests only)

## Notes

- Tests run with `-short` flag to exclude integration tests that require MongoDB
- All scripts work on both HEAD and HEAD~1 commits without modification
- Scripts are idempotent and can be run multiple times safely
- Git working directory remains clean after test execution
