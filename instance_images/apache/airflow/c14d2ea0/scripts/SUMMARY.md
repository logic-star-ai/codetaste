# Summary

This repository contains Apache Airflow 1.6.2, a platform to programmatically author, schedule and monitor data pipelines. The testing environment has been configured to run a representative subset of the test suite that operates with minimal external dependencies.

## System Dependencies

No additional system-level dependencies are required beyond the base Ubuntu environment. The setup uses:
- Python 3.8 (from pre-installed uv python distribution)
- SQLite database (no external database service needed)
- SequentialExecutor (no Celery/Redis needed)

System setup script (`/scripts/setup_system.sh`) only creates temporary directories with appropriate permissions.

## Project Environment

### Python Environment
- **Python Version**: 3.8.20 (cpython-3.8.20-linux-x86_64-gnu)
- **Virtual Environment**: Created in `~/airflow/venv`
- **Package Manager**: pip

### Key Dependencies
The setup installs compatibility-pinned versions to work around issues with modern Python 3.8:
- **MarkupSafe < 2.0**: Required for Jinja2 compatibility
- **Werkzeug < 1.0**: Required for Flask compatibility
- **itsdangerous < 2.0**: Required for Flask compatibility
- **SQLAlchemy >= 0.9.8, < 1.4**: Compatible with old Alembic version
- **WTForms == 2.1**: Required for Flask-WTF 0.12 compatibility
- **thrift == 0.11.0**: Version 0.9.x doesn't work with Python 3.8

### Setup Script Workarounds
The `setup_shell.sh` script handles several compatibility issues:
1. **Reserved keyword 'async'**: Temporarily patches setup.py to rename the `async` variable to `async_extra` (Python 3.7+ issue)
2. **Thrift version constraint**: Relaxes thrift version requirement during installation
3. **Dependency installation order**: Installs compatibility packages first to avoid conflicts

### Environment Variables
- `AIRFLOW_HOME`: `~/airflow`
- `AIRFLOW_CONFIG`: `~/airflow/unittests.cfg`
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN`: SQLite database path
- `AIRFLOW__CORE__EXECUTOR`: SequentialExecutor
- `AIRFLOW__TESTSECTION__TESTKEY`: testvalue (for configuration tests)

## Testing Framework

### Test Runner
- **Framework**: nose (nosetests)
- **Test Files**: tests/core.py, tests/configuration.py, tests/models.py
- **Total Tests**: 94 tests in representative subset

### Test Exclusions
The following tests are excluded as they require external services not available in the minimal setup:
- Hadoop/Hive tests (HiveServer2Test, TransferTests, HivePrestoTest)
- HDFS tests (WebHdfsSensorTest, WebHDFSHookTest)
- Database tests (MySqlTest, PostgresTest)
- Cloud service tests (S3HookTest)
- SSH tests (SSHHookTest)
- Import examples test (requires example DAGs to be fully functional)

### Test Workaround
The `run_tests` script temporarily renames `tests/__init__.py` during test execution to avoid import errors from docker and other optional dependencies that aren't installed.

### Test Results
- **Passed**: 63 tests
- **Failed**: 30 tests (mostly due to missing optional dependencies or environment-specific issues)
- **Skipped**: 1 test
- **Total**: 94 tests

### JSON Output Format
```json
{"passed": 63, "failed": 30, "skipped": 1, "total": 94}
```

## Additional Notes

### Compatibility Challenges
This is a legacy codebase from 2016 targeting Python 2.7/3.4. Running it on Python 3.8 required numerous compatibility workarounds:
- Modern versions of dependencies (Flask, Jinja2, SQLAlchemy, WTForms) have breaking changes
- The `async` keyword became reserved in Python 3.7
- Many test dependencies (docker-py, boto, pykerberos) are optional and not installed
- The test suite imports all operators eagerly, causing import errors for unavailable dependencies

### Script Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) are designed to work on both HEAD and HEAD~1 commits without modification. The setup_shell.sh script:
- Uses git to revert temporary patches to setup.py
- Creates idempotent installations (checks if airflow is already imported)
- Handles both fresh installs and re-runs gracefully

### Limitations
- Web UI tests may fail due to Flask/Werkzeug compatibility issues
- Email tests may have SMTP configuration issues
- Some core tests fail due to the test environment differences from the original Travis CI setup
- The test results are deterministic and consistent across runs
