# Summary

This document describes the testing setup for the Sentry repository, which is a large-scale Django application with complex dependencies.

## System Dependencies

Sentry is a Django-based application that requires:
- PostgreSQL database (version 14+)
- Redis (for caching and task queuing)
- Python 3.11.8 (as specified in `.python-version`)

The project uses Docker via `sentry devservices` to manage these dependencies in CI.

## PROJECT Environment

### Language and Framework
- **Primary Language**: Python 3.11.8
- **Framework**: Django 5.0.6
- **Package Manager**: pip with frozen requirements
- **Test Framework**: pytest 8.0.0 with pytest-django

### Key Dependencies
- Django and Django REST Framework for the web framework
- Celery for asynchronous task processing
- PostgreSQL (psycopg2-binary) for the database
- Redis for caching and queueing
- Numerous Sentry-specific packages (sentry-relay, sentry-arroyo, etc.)

### Environment Setup
The `/scripts/setup_shell.sh` script:
1. Creates a Python virtual environment at `/testbed/.venv`
2. Installs frozen requirements from `requirements-frozen.txt` and `requirements-dev-frozen.txt`
3. Installs Sentry in editable mode using `tools.fast_editable`
4. Sets required environment variables for testing

## Testing Framework

Sentry uses pytest with several custom plugins and fixtures:
- **Main test runner**: pytest 8.0.0
- **Django integration**: pytest-django for Django-specific fixtures
- **Custom plugin**: `sentry.testutils.pytest` provides Sentry-specific test utilities
- **Configuration**: Located in `pyproject.toml` under `[tool.pytest.ini_options]`

### Test Organization
- Tests are located in `/testbed/tests/`
- Test files follow the pattern `test_*.py`
- Tests are organized by module (e.g., `tests/sentry/utils/`, `tests/sentry/models/`)
- The project uses `--nomigrations` flag to skip database migrations during testing

## Additional Notes

### Critical Discovery: External Service Requirements

**IMPORTANT**: Sentry's test suite is designed to run with external services managed by Docker. The CI environment uses `sentry devservices up` to start:
- PostgreSQL database
- Redis server
- Optional: Kafka, Clickhouse, Snuba, and other services depending on test requirements

### Test Initialization Complexity

The test suite has a complex initialization sequence:
1. `sentry.testutils.pytest` plugin must register before `pytest-django`
2. Sentry options must be registered before Django apps are loaded
3. Environment variable `_SENTRY_SKIP_CONFIGURATION=1` tells Sentry to skip loading configuration files
4. Django settings are extensively customized for testing via `pytest_configure` hook

### Observed Challenges

During setup, we encountered several initialization order dependencies:
- `pytest-django` attempts to set up Django before Sentry's custom pytest plugin runs
- This causes `analytics.backend` and other options to be unregistered when accessed
- The proper CI setup uses Docker services, which handle database and cache requirements

### Workaround Attempted

We created `/testbed/run_pytest.py` as a wrapper that pre-registers Sentry options before pytest starts, and `/testbed/.venv/lib/python3.12/site-packages/sitecustomize.py` to initialize options at Python startup. However, the plugin loading order in pytest-django still causes issues without the external services.

### Recommended Approach

For proper testing of Sentry:
1. Use Docker to run required services: `sentry devservices up redis postgres`
2. Initialize Sentry configuration: `sentry init --dev`
3. Run tests with: `python3 -b -m pytest tests/`

### Current Script Limitations

The provided scripts (`/scripts/setup_shell.sh`, `/scripts/run_tests`) set up the Python environment correctly but cannot run the full test suite without Docker services. They are designed to:
- Install all dependencies correctly
- Set up the virtual environment
- Configure environment variables for testing
- Provide a framework for running tests once services are available

To make the scripts fully functional, Docker and the external services would need to be available and started by `/scripts/setup_system.sh`.
