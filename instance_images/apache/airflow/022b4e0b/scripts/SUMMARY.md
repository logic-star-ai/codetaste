# Summary

This repository contains Apache Airflow version 2.2.0.dev0, a platform for programmatically authoring, scheduling, and monitoring workflows. The testing infrastructure has been configured to run a representative subset of unit tests that validate core functionality without requiring external services.

## System Dependencies

The test environment requires minimal system-level dependencies:

- **Python**: 3.8 (compatible with Airflow 2.2.0.dev0 requirements)
- **Database**: SQLite (bundled with Python, no additional service required)
- **System packages**: None required for the selected test suite

The setup is designed to work with the existing system packages provided by the Ubuntu 24.04 environment. No additional system-level installations are necessary.

## Project Environment

### Python Version
- **Python 3.8.20** from `/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8`
- Chosen for best compatibility with Airflow 2.2.0.dev0 (requires Python ~=3.6)

### Virtual Environment
- Created at `/testbed/.venv` using Python venv module
- Isolated from system Python to ensure reproducible builds

### Dependencies
The project is installed in editable mode (`pip install -e .`) with the following key dependencies:

**Core Airflow Dependencies:**
- flask, flask-appbuilder, gunicorn (web framework)
- sqlalchemy, alembic (database ORM and migrations)
- pendulum, croniter (date/time handling)
- jinja2, markdown (templating and rendering)
- cryptography, pyjwt (security)

**Test Dependencies:**
- pytest ~=6.0 (test framework)
- pytest-cov, pytest-xdist, pytest-rerunfailures (pytest plugins)
- parameterized, freezegun, requests_mock (test utilities)
- mongomock, coverage, flaky (additional test tools)
- pandas, numpy (required by some test fixtures)

### Environment Variables
Key environment variables configured for testing:
- `AIRFLOW_HOME=/tmp/airflow_home` - Temporary airflow home directory
- `AIRFLOW__CORE__DAGS_FOLDER=/testbed/tests/dags` - Test DAGs location
- `AIRFLOW__CORE__UNIT_TEST_MODE=True` - Enables unit test mode
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN=sqlite:///$AIRFLOW_HOME/airflow.db` - SQLite database
- `AIRFLOW__CORE__EXECUTOR=SequentialExecutor` - Simple executor for testing
- `AWS_DEFAULT_REGION=us-east-1` - AWS region for provider tests

## Testing Framework

### Framework: pytest 6.2.5

The test suite uses pytest with custom plugins and fixtures defined in `/testbed/tests/conftest.py`:
- Automatic database initialization and reset
- SQL query tracing for debugging
- Custom fixtures for environment setup

### Test Selection

The `run_tests` script executes a representative subset of tests focusing on core functionality:
- `tests/core/test_core.py` - Core Airflow functionality
- `tests/utils/test_dates.py` - Date utility tests
- `tests/utils/test_timezone.py` - Timezone handling tests
- `tests/models/test_dagbag.py` - DAG bag model tests
- `tests/models/test_baseoperator.py` - Base operator tests
- `tests/api/common/experimental/test_pool.py` - API pool tests

These tests provide good coverage of essential functionality and complete within 15-30 seconds, making them suitable for rapid validation.

### Test Output Format

The `run_tests` script outputs exactly one JSON line to stdout:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

Results are parsed from:
1. pytest's summary line (primary method)
2. JUnit XML report fallback (if summary parsing fails)

### Running Tests

Execute the full test workflow:
```bash
cd /testbed
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

Or in a single command:
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Additional Notes

### Installation Challenges

1. **Constraint conflicts**: The Apache Airflow constraints file for version 2-2 contains some version conflicts (e.g., croniter). The installation falls back to installing without constraints, which works successfully.

2. **mysqlclient compilation**: The optional `mysqlclient` package fails to build due to missing MySQL development headers. This is expected and doesn't affect the test suite since we're using SQLite.

3. **Provider packages**: Some Airflow provider packages are installed from PyPI rather than source, which is acceptable for the test suite.

### Test Stability

- Tests run deterministically with SQLite backend
- Some tests may fail due to timing issues (e.g., process timeout tests)
- The test suite is representative but not exhaustive (full suite would take much longer)
- Tests work consistently across commits (validated on HEAD and HEAD~1)

### Portability

The scripts are designed to be portable and work across different commits:
- No hardcoded commit references
- Dynamic installation based on setup.py at each commit
- Environment setup is idempotent and safe to run multiple times
- All modifications are made to ignored files (.venv, build artifacts, cache)

### Performance

- Initial setup (including pip install): ~2-3 minutes
- Subsequent setups (with cached dependencies): ~10-20 seconds
- Test execution: ~15-30 seconds
- Total workflow time: ~3-5 minutes for first run, ~30-60 seconds for subsequent runs
