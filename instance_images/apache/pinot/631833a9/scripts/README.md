# Apache Pinot Test Scripts

This directory contains scripts to set up and run tests for the Apache Pinot project.

## Scripts

### setup_system.sh
System-level setup script that must be run with sudo. For this project, it doesn't need to perform any actions as unit tests don't require system services.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### setup_shell.sh
Shell environment setup script that configures Java 11, Maven, and builds the project. This script MUST be sourced, not executed.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

### run_tests
Executes the test suite and outputs results in JSON format. Must be run after setup_shell.sh has been sourced.

**Usage:**
```bash
/scripts/run_tests
```

**Output:** JSON line with format:
```json
{"passed": N, "failed": N, "skipped": N, "total": N}
```

## Complete Test Execution

To run the complete test suite from a clean state:

```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Notes

- Tests take approximately 2.5 minutes to run
- Build takes approximately 1-3 minutes depending on Maven cache
- Scripts are designed to work on both HEAD and HEAD~1 commits
- Java 11 is required (automatically configured by setup_shell.sh)
