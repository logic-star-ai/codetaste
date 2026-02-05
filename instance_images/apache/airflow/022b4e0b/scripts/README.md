# Apache Airflow Test Scripts

This directory contains scripts to set up and run tests for Apache Airflow.

## Scripts

### `/scripts/setup_system.sh`
System-level setup script that must be run with `sudo`. Creates necessary directories and sets permissions for the test environment.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### `/scripts/setup_shell.sh`
Shell environment setup script that configures Python virtual environment, installs dependencies, and sets environment variables. This script must be **sourced**, not executed.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

### `/scripts/run_tests`
Runs a representative subset of Airflow unit tests and outputs results in JSON format. Assumes the environment has been set up via the previous scripts.

**Usage:**
```bash
/scripts/run_tests
```

**Output Format:**
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Complete Workflow

To run tests from a clean state:

```bash
cd /testbed
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

Or as a single command:
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Requirements

- Python 3.8+ available in `/opt/uv-python/`
- Ubuntu 24.04 or compatible Linux distribution
- Git repository at `/testbed/`

## Notes

- The scripts are idempotent and safe to run multiple times
- Virtual environment is created at `/testbed/.venv`
- Airflow home directory is set to `/tmp/airflow_home`
- Tests use SQLite database (no external database required)
- All changes are made to ignored files only (git status remains clean)
- Scripts work across different commits without modification

## Test Selection

The test suite runs the following test files:
- `tests/core/test_core.py` - Core functionality tests
- `tests/utils/test_dates.py` - Date utility tests
- `tests/utils/test_timezone.py` - Timezone handling tests
- `tests/models/test_dagbag.py` - DAG bag model tests
- `tests/models/test_baseoperator.py` - Base operator tests
- `tests/api/common/experimental/test_pool.py` - API pool tests

Total execution time: 15-30 seconds

## Troubleshooting

If tests fail to run:
1. Ensure `/testbed/` is a clean git checkout
2. Verify Python 3.8 is available at `/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8`
3. Check that `/tmp/airflow_home` is writable
4. Run `git clean -xdff` to remove all generated files

For more details, see `/scripts/SUMMARY.md`.
