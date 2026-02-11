# Test Environment Setup Scripts for Apache Pegasus

## Overview

These scripts configure the development environment and run tests for Apache Pegasus.

## Script Execution Order

1. **setup_system.sh** - Run with sudo to configure system-level settings
2. **setup_shell.sh** - Source to set up the shell environment and build the project
3. **run_tests** - Execute the test suite and output JSON results

## Usage

### Standard Usage (Clean Environment)

```bash
cd /testbed
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

### Quick Usage (Already Set Up)

```bash
source /scripts/setup_shell.sh && /scripts/run_tests
```

## What Each Script Does

### setup_system.sh
- Sets system ulimits (stack size, open files, core dumps)
- No package installation (done separately)
- Quick execution (<1 second)

### setup_shell.sh
- Sets environment variables (JAVA_HOME, LD_LIBRARY_PATH, etc.)
- Creates symlinks for thrift binary
- Builds thirdparty dependencies if needed (~30-60 minutes first run)
- Builds Pegasus with tests if needed (~20-40 minutes first run)
- Idempotent: safe to run multiple times

### run_tests
- Runs 7 representative test modules
- Modules selected to finish in ~15 minutes
- Parses XML test results
- Outputs JSON: {"passed": N, "failed": M, "skipped": K, "total": T}

## Test Modules

The following test modules are included in the test subset:
- base_test
- dsn_utils_tests
- dsn_runtime_tests
- dsn_http_test
- dsn_client_test
- dsn_aio_test
- pegasus_unit_test

## Notes

- First run requires significant build time (~1-2 hours total)
- Subsequent runs reuse cached builds
- Scripts work on both HEAD and HEAD~1 commits
- All build artifacts are in git-ignored directories
