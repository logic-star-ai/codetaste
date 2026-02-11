# Summary

This repository contains PrestaShop, an open-source e-commerce platform written in PHP. The testing setup has been configured to run the comprehensive unit test suite using PHPUnit 10.

## System Dependencies

### Core Requirements
- **PHP 8.1.34** - Installed from ondrej/php PPA
- **MySQL 8.0.44** - Database server for test data
- **Composer 2.7.1** - PHP dependency manager

### PHP Extensions
The following PHP extensions are required and installed:
- php8.1-cli
- php8.1-common
- php8.1-curl
- php8.1-dom
- php8.1-gd (graphics library)
- php8.1-intl (internationalization)
- php8.1-mbstring (multibyte string)
- php8.1-mysql
- php8.1-xml
- php8.1-zip

### System Services
- MySQL/MariaDB server (started via `/scripts/setup_system.sh`)

## Project Environment

### Configuration Files
- **`/testbed/app/config/parameters.php`** - Created automatically by setup_shell.sh with test database credentials
  - Database: `prestashop` (prefixed with `test_` during tests)
  - User: `root`
  - Password: (empty)
  - Host: `127.0.0.1`
  - Prefix: `ps_`

### Dependencies
- **Composer dependencies**: ~680 packages installed in `/testbed/vendor/`
- Dependencies are installed automatically by `setup_shell.sh` if not present
- Installation is idempotent - safe to run multiple times

### Environment Variables
- `_PS_ROOT_DIR_=/testbed`
- `PS_DOMAIN=localhost`
- Tests run with `_PS_IN_TEST_=true` which modifies behavior:
  - Database name is prefixed with `test_`
  - Test-specific resource directories are used

## Testing Framework

### Test Suite
- **Framework**: PHPUnit 10.5.38
- **Test Type**: Unit tests
- **Test Count**: 4,367 tests with 9,487 assertions
- **Location**: `/testbed/tests/Unit/`
- **Configuration**: `/testbed/tests/Unit/phpunit.xml`

### Test Execution
The tests are executed with the following configuration:
- PHP timezone set to UTC (`-d date.timezone=UTC`)
- Memory limit set to unlimited (`-d memory_limit=-1`)
- No code coverage collection (`--no-coverage`)
- XML results logged in JUnit format for parsing

### Test Results
Tests are parsed from JUnit XML format and output as JSON with the following structure:
```json
{
  "passed": 4365,
  "failed": 0,
  "skipped": 2,
  "total": 4367
}
```

### Expected Results
- **Total Tests**: 4,367
- **Passed**: ~4,365
- **Skipped**: ~2
- **Failed**: 0
- **Execution Time**: ~9 seconds

## Scripts

### `/scripts/setup_system.sh`
- Runs with `sudo` to start system services
- Starts MySQL/MariaDB service if available
- Does NOT install packages (packages are pre-installed)
- Must be idempotent and safe to run multiple times

### `/scripts/setup_shell.sh`
- Configures shell environment for running tests
- Creates `/testbed/app/config/parameters.php` if missing
- Installs Composer dependencies if needed
- Sets required environment variables
- Must be sourced, not executed: `source /scripts/setup_shell.sh`

### `/scripts/run_tests`
- Executes the PHPUnit test suite
- Outputs JSON results as the final line of stdout
- Requires environment to be set up first via `setup_shell.sh`
- Logs test progress to stderr

### `/scripts/parse_phpunit_xml.py`
- Python 3 script to parse JUnit XML output
- Extracts test statistics and outputs JSON

## Additional Notes

### Performance
- Unit tests complete in approximately 9 seconds
- Tests are self-contained and don't require a full PrestaShop installation
- Tests use in-memory configurations where possible

### Compatibility
- All scripts work on both HEAD and HEAD~1 without modifications
- The repository uses git and all tracked files remain unchanged after test runs
- Only generated files (vendor/, cache/, parameters.php) are created

### Known Issues
- MySQL service in container environment required manual initialization
- Linux Native AIO warnings from MySQL can be safely ignored (container limitation)
- Some PHPUnit deprecation warnings are expected from the test suite itself
- The `.gitkeep` file in `var/cache/` should not have its permissions changed

### Test Invocation
To run tests in a clean environment:
```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

The final line of output will be valid JSON with test results.
