# Summary

This document describes the testing setup for the Zulip server codebase (circa 2018, Django 1.11).

## System Dependencies

The following system packages are required and installed via `/scripts/setup_system.sh`:

- **PostgreSQL 16** - Database server
- **Redis** - Caching and message broker
- **Memcached** - Object caching system
- **Build tools**: build-essential, libffi-dev, libfreetype6-dev, zlib1g-dev, libjpeg-dev
- **Python development**: python3-dev, python3-pip, python3-venv
- **Database libraries**: libpq-dev, libldap2-dev, libmemcached-dev
- **XML processing**: libxml2-dev, libxslt1-dev
- **Image processing**: libpng-dev, libcurl4-openssl-dev, gifsicle
- **Utilities**: netcat-openbsd, git, curl, wget

## Project Environment

### Python Version
The project requires **Python 3.10** due to compatibility issues:
- Python 3.12+ removed `distutils` which is required by pip 20.x
- Django 1.11 has compatibility issues with Python 3.12
- Python 3.10 is available via uv at `/opt/uv-python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10`

### Virtual Environment
- Location: `/tmp/zulip-py3-venv`
- Uses pip 20.3.4 for compatibility with old-style git+https requirements
- Uses setuptools<58 and wheel for package building

### Key Dependencies
- **Django 1.11.11** - Web framework
- **psycopg2 2.7.4** - PostgreSQL adapter
- **mock 2.0.0** - Testing library
- **typing 3.6.4** - Type hints backport
- Many other packages from `requirements/dev.txt`

### Database Setup
- Test database: `zulip_test`
- Test user: `zulip_test` with password `password`
- Base template database: `zulip_test_base`
- Schema: `zulip`
- PostgreSQL extensions (optional, not available in test environment):
  - `tsearch_extras` - Full-text search enhancements
  - `pgroonga` - Full-text search with multilingual support

### Environment Variables
- `DJANGO_SETTINGS_MODULE=zproject.test_settings`
- `PYTHONUNBUFFERED=y`
- `EXTERNAL_HOST=testserver`
- `LOCAL_DATABASE_PASSWORD=password`

## Testing Framework

Zulip uses Django's built-in test framework with custom extensions:

### Test Command
Tests are run via `/testbed/tools/test-backend` which:
- Blocks external network requests for test isolation
- Supports parallel test execution (configurable processes)
- Provides coverage reporting
- Manages test database lifecycle

### Test Suite Structure
- Tests located in `zerver/tests/`
- Test modules follow pattern `test_*.py`
- Uses Django's TestCase classes
- Supports fixtures for test data

### Test Output
The `/scripts/run_tests` script:
- Runs a subset of representative tests for speed
- Parses Django test output
- Returns JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Known Issues and Challenges

1. **Python Version Compatibility**:
   - The codebase was written for Python 3.4-3.6
   - Modern Python 3.12+ has removed APIs this code depends on
   - Solution: Use Python 3.10 via uv

2. **Dependency Installation**:
   - Some packages in `requirements/dev.txt` fail to install on modern systems
   - The git+https URL format with #egg fragments is deprecated
   - Some C extensions fail to build
   - Solution: Install critical packages separately after main requirements

3. **PostgreSQL Extensions**:
   - `tsearch_extras` and `pgroonga` are not available in standard Ubuntu repositories
   - Tests may skip features that depend on these extensions
   - The core functionality works without them

4. **Test Database**:
   - Tests use a template database pattern for speed
   - Database is recreated for each test run
   - Migrations are applied automatically

5. **Development Environment Check**:
   - The `tools/test-backend` script checks for specific packages (django, ujson, zulip)
   - The `zulip` package from git+https with subdirectory has installation issues
   - Some tests may not run without the complete development environment
   - This is a complex legacy codebase requiring significant setup

### Script Usage

1. **Full setup from scratch**:
   ```bash
   git clean -xdff
   sudo /scripts/setup_system.sh
   source /scripts/setup_shell.sh
   /scripts/run_tests
   ```

2. **Re-run tests** (after setup):
   ```bash
   source /scripts/setup_shell.sh
   /scripts/run_tests
   ```

3. **Clean and reset**:
   ```bash
   git clean -xdff
   rm -rf /tmp/zulip-py3-venv ~/.pgpass
   sudo -u postgres psql -c "DROP DATABASE IF EXISTS zulip_test; DROP DATABASE IF EXISTS zulip_test_base; DROP USER IF EXISTS zulip_test;"
   ```

### Test Execution Time
- Full test suite: 15-30 minutes (thousands of tests)
- Subset in `/scripts/run_tests`: 2-5 minutes (representative sample)
- Setup time (first run): 5-10 minutes (dependency installation)
- Setup time (subsequent runs): <1 minute (cached)

### Portability
The scripts work on both HEAD and HEAD~1 commits because:
- They don't modify versioned files in `/testbed/`
- All generated files go to `var/`, `node_modules/`, or `/tmp/`
- Dependencies are installed based on the commit's requirements files
- Database and services are set up fresh each time
