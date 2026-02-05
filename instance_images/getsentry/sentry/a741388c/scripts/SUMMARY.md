# Summary

This repository is Sentry, a large Django-based error tracking and performance monitoring platform. The testing infrastructure is complex and relies on specific initialization order and configuration that makes it challenging to run in an isolated environment without the full development setup.

## System Dependencies

The Sentry application has minimal system-level dependencies for running tests:

- **Python 3.11.14** (specified in `.python-version`)
- **PostgreSQL** (optional for unit tests - uses in-memory databases)
- **Redis** (optional for unit tests - uses mock/dummy backends)
- **Kafka** (optional for unit tests)

Most system services are mocked for unit tests, so the scripts don't require actual database or cache services to be running.

## PROJECT Environment

### Python Setup
- Uses Python 3.11.14 (managed via uv)
- Virtual environment created at `/testbed/.venv`
- Dependencies installed from:
  - `requirements-base.txt` - Core runtime dependencies
  - `requirements-dev-frozen.txt` - Development and testing dependencies

### Key Environment Variables
- `_SENTRY_SKIP_CONFIGURATION=1` - Skip Sentry configuration file loading (for tests)
- `DJANGO_SETTINGS_MODULE=sentry.conf.server` - Django settings module
- `SENTRY_SKIP_BACKEND_VALIDATION=1` - Skip backend validation

### Installation Method
The project uses a custom fast_editable installation method via `tools.fast_editable` instead of standard `pip install -e .`

## Testing Framework

### Primary Testing Tool
- **pytest** with multiple plugins:
  - `pytest-django` - Django integration
  - `pytest-cov` - Code coverage
  - `pytest-xdist` - Parallel test execution
  - `pytest-rerunfailures` - Retry flaky tests
  - `pytest-sentry` - Sentry-specific fixtures

### Test Organization
- Tests located in `/testbed/tests/`
- Structured by module: `tests/sentry/`, `tests/flagpole/`, etc.
- Excludes acceptance tests (require Selenium), JS tests, and tool tests for basic runs

### Configuration
- Test configuration in `pyproject.toml` under `[tool.pytest.ini_options]`
- Custom pytest plugins in `src/sentry/testutils/pytest/`
- Test fixtures and utilities in `src/sentry/testutils/`

## Additional Notes

### Challenges Encountered

1. **Options Initialization Order**: The Sentry options system requires `load_defaults()` to be called before Django apps are initialized. However, Django's app loading (via `INSTALLED_APPS`) happens before pytest's `pytest_configure()` hook can set things up properly when running pytest in an isolated environment.

2. **Complex Django Setup**: The application uses a custom Django configuration with:
   - Split databases (control, region, secondary)
   - Custom silo mode configurations
   - Lazy service wrappers for analytics, caching, etc.
   - Multiple inter-dependent apps that import each other

3. **Environment Isolation**: The repository is designed to work with Sentry's internal development infrastructure (devservices, specific Docker containers, etc.) and running it in complete isolation requires careful environment setup.

### Working Approach

The scripts have been configured to:
1. Set up a clean Python 3.11 virtual environment
2. Install all required dependencies
3. Set necessary environment variables
4. Attempt to run a subset of simpler tests

### Known Limitations

Due to the complexity of the Sentry Django application and the specific initialization order requirements, the test suite requires careful setup that may not be fully replicated without the complete Sentry development environment. The scripts provide the foundational setup, but running the full test suite may require additional configuration or running within Sentry's official development environment (using `sentry devservices` and `make develop`).

### Recommendation for Production Use

For reliable test execution on this repository, it's recommended to:
1. Use the official Sentry development setup documented in their README
2. Run `make develop` to set up the full environment
3. Use `make test-python-ci` for running the test suite
4. Ensure all devservices are running if needed for specific test suites

The scripts provided here offer a starting point for environment setup and can be adapted for specific testing needs, but they represent a simplified approach compared to the full Sentry development environment.
