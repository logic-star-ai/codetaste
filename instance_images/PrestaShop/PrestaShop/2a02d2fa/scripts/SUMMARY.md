# Summary

This repository contains PrestaShop, an open-source e-commerce platform written in PHP. The test environment has been configured to run PHPUnit unit tests across the codebase.

## System Dependencies

The following system-level dependencies are required:

- **PHP 8.1** with extensions:
  - php8.1-cli
  - php8.1-mbstring
  - php8.1-intl
  - php8.1-gd
  - php8.1-xml
  - php8.1-curl
  - php8.1-zip
  - php8.1-mysql
  - php8.1-bcmath
  - JSON support (built-in)
  - DOM, fileinfo, iconv, simplexml, openssl (all included)

- **MariaDB/MySQL** database server
  - Used for integration tests (though unit tests run without DB)
  - Test database: `prestashop`
  - Test credentials: root/password

- **Composer** 2.x for PHP dependency management

## PROJECT Environment

The project is a Symfony 6.4-based application requiring:

1. **Composer dependencies**: Installed via `composer install` (283+ packages)
2. **Configuration**: `app/config/parameters.yml` file with database connection details
3. **PHP Settings**:
   - Timezone set to UTC
   - Symfony deprecations helper disabled for cleaner test output
   - Memory limit: unlimited for integration tests

## Testing Framework

**Primary Framework**: PHPUnit 10.x

The test suite structure:
- **Unit Tests**: Located in `tests/Unit/`
  - Configuration: `tests/Unit/phpunit.xml`
  - ~4,367 tests covering core PHP classes
  - No database required
  - Test results: 4,365 passed, 0 failed, 2 skipped
  - Execution time: ~9-10 seconds

- **Integration Tests**: Located in `tests/Integration/`
  - Requires database setup and initialization
  - Uses Behat for behavior-driven tests
  - Not included in the current test run for time constraints

- **UI/E2E Tests**: Located in `tests/UI/`
  - Uses Playwright/Mocha for browser automation
  - Not included in current setup

## Additional Notes

**Test Runner Design**:
- The `/scripts/run_tests` script runs only unit tests to complete within the 15-minute window
- JSON output format: `{"passed": int, "failed": int, "skipped": int, "total": int}`
- Parses PHPUnit JUnit XML output and text output as fallback

**Environment Challenges**:
- Container doesn't use systemd, so MariaDB is started via `service` command
- Database is configured on first system setup
- The scripts are designed to work on both HEAD and HEAD~1 commits without modification

**Portability**:
- All scripts use absolute paths and avoid assumptions about the working directory
- `setup_shell.sh` is idempotent and checks for existing installations
- Test configuration is created dynamically if missing
- Works across different commits of the repository
