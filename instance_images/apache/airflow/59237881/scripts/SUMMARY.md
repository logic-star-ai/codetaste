# Summary

This directory contains scripts to configure the development environment and run validation tests for the Apache Airflow repository.

## System Dependencies

The following system-level dependencies are required and installed by `/scripts/setup_system.sh`:

- **libmysqlclient-dev** - MySQL client library for building mysqlclient Python package
- **pkg-config** - Helper tool for compiling applications and libraries
- **libpq-dev** - PostgreSQL development libraries
- **libssl-dev** - SSL/TLS development libraries
- **libffi-dev** - Foreign Function Interface library development files
- **libkrb5-dev** - Kerberos development libraries
- **libsasl2-dev** - SASL2 development libraries
- **libldap2-dev** - LDAP development libraries

These dependencies are required for building various Python packages that Airflow depends on, particularly database drivers and security-related packages.

## PROJECT Environment

### Python Version
- **Python 3.9** (from `/opt/uv-python/cpython-3.9.25-linux-x86_64-gnu/bin/python3.9`)
- Airflow 2.4.0 supports Python 3.7-3.10

### Virtual Environment
- Created at `/tmp/airflow_venv`
- Isolated from the system Python to avoid conflicts
- Uses pip for package management

### Key Environment Variables
- `AIRFLOW_HOME=/tmp/airflow_home` - Home directory for Airflow configuration and metadata
- `AIRFLOW__CORE__UNIT_TEST_MODE=True` - Enables unit test mode
- `AIRFLOW__CORE__LOAD_EXAMPLES=False` - Disables example DAGs
- `AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False` - Disables default connections
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN=sqlite:///...` - Uses SQLite for testing
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:///...` - Database connection string
- `INSTALL_PROVIDERS_FROM_SOURCES=true` - Installs providers from source code
- `AWS_DEFAULT_REGION=us-east-1` - Default AWS region for tests

### Dependency Management
The setup script installs Airflow with the `[devel]` extra, which includes:
- Core Airflow dependencies
- Development tools (pytest, mypy, flake8, etc.)
- Testing frameworks (pytest-cov, pytest-xdist, freezegun, etc.)
- Documentation tools
- Provider dependencies for mysql

### Compatibility Fixes
To ensure compatibility with Airflow 2.4, the following version constraints are applied:
- `pendulum>=2.0,<3.0` - Airflow 2.4 requires Pendulum 2.x (Pendulum 3.x has breaking API changes)
- `werkzeug>=2.0,<2.3` - Compatible version for Flask dependencies
- `flask-wtf<1.1` - Compatible version for form handling

### Database
- SQLite is used for testing (no external database service required)
- Database is initialized with `airflow db init` during setup
- Database file stored at `/tmp/airflow_home/airflow.db`

## Testing Framework

### Test Runner
- **Framework**: pytest 6.x
- **Test Selection**: Representative subset of tests focusing on:
  - Utility tests (`tests/utils/test_timezone.py`)
  - Model tests (`tests/models/test_pool.py`, `tests/models/test_variable.py`, `tests/models/test_timestamp.py`)
  - Executor tests (`tests/executors/test_executor_loader.py`, `tests/executors/test_sequential_executor.py`)
  - CLI tests (`tests/cli/commands/test_info_command.py`)

### Test Configuration
- Pytest configuration in `/testbed/pytest.ini`
- Verbose output (`-v`) for detailed test results
- Short tracebacks (`--tb=line`) for concise error reporting
- Test discovery pattern: `test_*.py`

### Output Format
The test runner outputs results in JSON format:
```json
{
  "passed": <number>,
  "failed": <number>,
  "skipped": <number>,
  "total": <number>
}
```

### Running Tests
Tests are executed via `/scripts/run_tests` which:
1. Changes to `/testbed` directory
2. Runs pytest with selected test files
3. Captures and parses test output
4. Outputs JSON summary to stdout
5. Diagnostic output goes to stderr

## Additional Notes

### Test Execution Challenges
During setup, several challenges were encountered:

1. **Dependency Compatibility**: Airflow 2.4 was released before some newer versions of dependencies (pendulum 3.x, werkzeug 2.3+) that have breaking changes. Version constraints were added to ensure compatibility.

2. **System Libraries**: Many Python packages require system-level development libraries to build native extensions. All required libraries are installed in `setup_system.sh`.

3. **Database Initialization**: Tests require the Airflow database schema to be initialized before running. This is handled automatically in `setup_shell.sh`.

4. **Provider Dependencies**: Some tests import provider-specific code. Setting `INSTALL_PROVIDERS_FROM_SOURCES=true` ensures providers are available from the source tree.

### Idempotency
All scripts are designed to be idempotent:
- `setup_system.sh`: Installs only if packages are not already present
- `setup_shell.sh`: Creates virtual environment only if it doesn't exist, marks setup complete with a flag file
- `run_tests`: Can be run multiple times with consistent results

### Portability
The scripts are portable across commits:
- No hardcoded paths to testbed-specific files
- Only use standard directories and configuration files
- Work on both HEAD and HEAD~1 without modification
- All temporary files are stored outside `/testbed`

### Performance
- Virtual environment creation and dependency installation: ~2-5 minutes (first time)
- Subsequent runs (with cached venv): ~5-10 seconds for setup
- Test execution: Variable (depends on tests selected, typically 30-60 seconds for the subset chosen)

### Limitations
- Tests requiring external services (PostgreSQL, MySQL, Redis, etc.) are not included
- Only a subset of tests are run to keep execution time reasonable (<15 minutes)
- Some tests may fail due to missing optional dependencies
