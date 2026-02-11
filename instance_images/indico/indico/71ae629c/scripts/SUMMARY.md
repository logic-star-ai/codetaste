# Summary

This document describes the testing environment setup for the Indico project, a Python 2.7 legacy codebase.

## System Dependencies

The following system-level dependencies were installed:

- **PostgreSQL 16**: Database server for test execution (with `postgresql-contrib` and `libpq-dev`)
- **Python 2.7.18**: Built from source at `/opt/python2.7` (Ubuntu 24.04 no longer provides Python 2.7 packages)
- **Build essentials**: `build-essential`, `libxml2-dev`, `libxslt1-dev`, `libjpeg-dev`, `libfreetype6-dev`, `zlib1g-dev`

### PostgreSQL Setup

PostgreSQL needs to be running before tests can execute. The `setup_system.sh` script handles starting PostgreSQL if it's not already running.

## Project Environment

### Python Version

The project requires **Python 2.7** due to Python 2 syntax throughout the codebase (e.g., `print` statements, `except Exception, e:` syntax). Python 2.7.18 was compiled from source and installed to `/opt/python2.7`.

### Virtual Environment

A Python 2.7 virtualenv is created at `/testbed/.venv` containing all project dependencies.

### Key Dependencies

- **Testing**: pytest==4.6.11, pytest-cov, pytest-mock, pytest-catchlog, pytest-localserver
- **Database**: SQLAlchemy==1.1.4, psycopg2-binary, Flask-SQLAlchemy, zope.sqlalchemy==0.7.7
- **ZODB**: ZODB3, ZEO, BTrees (for legacy ZODB support)
- **Web Framework**: Flask==1.1.4, Flask-PluginEngine<0.4, Flask-Multipass
- **Utilities**: babel, lxml, pytz, python-dateutil, freezegun, alembic, redis==2.10.5

### Special Considerations

1. **MaKaC Symlink**: The codebase requires a symlink from `/testbed/MaKaC` to `/testbed/indico/MaKaC` for the legacy module structure.

2. **Version Constraints**: Many dependencies have specific version requirements due to Python 2.7 compatibility:
   - SQLAlchemy 1.1.4 (later versions removed SessionExtension)
   - zope.sqlalchemy 0.7.7 (later versions removed ZopeTransactionExtension)
   - redis 2.10.5 (later versions changed API)
   - Flask-PluginEngine<0.4 (later versions use Python 3 f-strings)

3. **Git Dependencies**: flask-pluginengine and flask-multipass from git repos need older versions to work with Python 2.7.

## Testing Framework

The project uses **pytest 4.6.11** (last version supporting Python 2.7) with the following plugins:
- pytest-cov for coverage reporting
- pytest-mock for mocking
- pytest-catchlog for log capture
- pytest-localserver for local server testing

### Test Configuration

Tests are configured via `/testbed/pytest.ini`:
- Test files must end with `*_test.py`
- Coverage reporting enabled with HTML output
- Several directories excluded from test collection (legacy tests, MaKaC, htdocs, etc.)

### Test Execution

Tests are executed using the `/scripts/run_tests` script which:
1. Runs `pytest -v` to execute all tests
2. Captures and parses the output
3. Produces a JSON summary with format: `{"passed": int, "failed": int, "skipped": int, "total": int}`

## Additional Notes

### Obstacles Encountered

1. **Python 2.7 Availability**: Python 2.7 is EOL and not available in Ubuntu 24.04 repositories. Had to compile from source.

2. **Dependency Hell**: Many packages have conflicting versions or lack Python 2.7 support in recent versions. Required careful version pinning.

3. **Mixed Python 2/3 Code**: The codebase has `from __future__` imports suggesting partial Python 3 compatibility, but setup.py and some core files use Python 2-only syntax.

4. **ZODB Legacy**: The project uses ZODB (Zope Object Database) which adds complexity to the dependency tree.

5. **Missing Dependencies**: Not all dependencies from `requirements.txt` could be cleanly installed due to:
   - Some packages no longer supporting Python 2.7
   - Git dependencies using Python 3 syntax
   - Build failures for certain C extensions

### Script Portability

The scripts in `/scripts/` are designed to work on both `HEAD` and `HEAD~1` commits without modification. They:
- Use dynamic dependency installation
- Don't rely on commit-specific file structures
- Handle missing dependencies gracefully
- Create necessary symlinks and environment variables

### Running Tests

To run tests:
```bash
cd /testbed
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

The final line of output will be JSON with test results.
