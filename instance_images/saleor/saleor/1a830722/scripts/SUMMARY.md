# Summary

This document describes the testing setup for the Saleor e-commerce platform, a Python/Django-based headless GraphQL commerce platform.

## System Dependencies

The following system-level dependencies are required and installed via `/scripts/setup_system.sh`:

- **PostgreSQL 16**: Main database system for Django models
- **Redis**: Cache backend and Celery message broker
- **libmagic1**: Required for python-magic file type detection
- **libpq-dev**: PostgreSQL development headers for psycopg2
- **libpango-1.0-0 / libpangocairo-1.0-0**: Required for WeasyPrint (PDF generation)

The setup script also configures:
- PostgreSQL user `saleor` with password `saleor`
- PostgreSQL database `saleor`
- Starts both PostgreSQL and Redis services

## Project Environment

The project uses:

- **Language**: Python 3.9 (as specified in pyproject.toml: `python = "~3.9"`)
- **Package Manager**: Poetry (version 1.7.1)
- **Virtual Environment**: `.venv` directory in the project root
- **Framework**: Django 3.2.23
- **Test Framework**: pytest with pytest-django and pytest-xdist (parallel execution)

### Key Python Dependencies

- **Django 3.2.23**: Web framework
- **GraphQL/Graphene**: GraphQL API implementation
- **Celery 5.3**: Async task processing
- **Poetry**: Dependency management
- **pytest 7.4**: Test framework with various plugins

### Environment Variables

The following environment variables are configured for testing:

- `DATABASE_URL`: postgres://saleor:saleor@localhost:5432/saleor
- `SECRET_KEY`: test-secret-key-for-testing
- `DEBUG`: True
- `ALLOWED_CLIENT_HOSTS`: localhost,127.0.0.1
- `CELERY_BROKER_URL`: redis://localhost:6379/0
- `CACHE_URL`: redis://localhost:6379/1
- `DEFAULT_CHANNEL_SLUG`: main

## Testing Framework

### Test Configuration

Tests are configured via:
- `setup.cfg`: pytest configuration with settings `--ds=saleor.tests.settings`
- `conftest.py`: pytest fixtures and plugins
- Test settings: `saleor/tests/settings.py`

### Test Execution

The test suite uses:
- **pytest** with parallel execution via `pytest-xdist` (`-n auto`)
- **pytest-django** for Django integration
- **Database**: Uses PostgreSQL in test mode
- **Socket blocking**: `--disable-socket --allow-unix-socket` to prevent external network calls

### Test Subset

The `/scripts/run_tests` script executes a representative subset of tests covering:
- `saleor/discount/tests/` - Discount and voucher logic
- `saleor/account/tests/` - User account management
- `saleor/app/tests/` - App integration
- `saleor/shipping/tests/` - Shipping methods
- `saleor/warehouse/tests/` - Warehouse management

This subset was selected to:
- Complete within 15 minutes (~3-4 minutes typical runtime)
- Cover core business logic
- Exclude slow e2e tests
- Provide good test coverage across modules
- Total: ~399 tests

### Test Output

The test runner outputs results in JSON format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Script Usage

### Complete Test Workflow

```bash
# Clean workspace and run all setup + tests
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

### Individual Scripts

1. **System Setup** (requires sudo):
   ```bash
   sudo /scripts/setup_system.sh
   ```

2. **Shell Environment** (must be sourced):
   ```bash
   source /scripts/setup_shell.sh
   ```

3. **Run Tests** (after sourcing setup_shell.sh):
   ```bash
   /scripts/run_tests
   ```

## Additional Notes

### Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification.

### Idempotency

The `setup_shell.sh` script is idempotent and uses marker files (`.pip_upgraded`, `.deps_installed`, `.project_installed`) to avoid redundant installations when run multiple times.

### Migrations

Django migrations are automatically applied during the shell setup phase to ensure the database schema is current.

### Performance

- Virtual environment is created with Python 3.9
- Poetry installs dependencies from the lock file for reproducibility
- Tests run in parallel using all available CPU cores (`-n auto`)
- Database connection pooling is configured with connection persistence

### Known Warnings

- SECRET_KEY warning: Expected in test mode, a random key is generated
- libmagic ImportError: Handled, required for file type detection in production features but tests pass

### Test Collection

Total test suite contains 11,718 tests. The subset executed covers approximately 3.4% of the full test suite but provides good coverage of core functionality.
