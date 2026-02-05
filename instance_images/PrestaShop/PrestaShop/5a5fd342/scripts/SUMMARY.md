# Summary

This document describes the testing setup for PrestaShop, an open-source e-commerce platform written in PHP.

## System Dependencies

The following system-level dependencies are required:

- **PHP 8.1+** with extensions:
  - curl
  - dom (xml)
  - fileinfo (part of common)
  - gd
  - iconv (part of common)
  - intl
  - json (part of common)
  - mbstring
  - mysql (mysqli, pdo_mysql)
  - openssl (part of common)
  - simplexml (xml)
  - zip

- **MySQL/MariaDB 5.6+**: Database server for test data
  - Test database: `prestashop_test`
  - Test user: `prestashop` / `prestashop`

- **Composer**: PHP dependency manager (version 2.9.4+)

## PROJECT Environment

The project uses:
- **PHP**: Version 8.1.34 (required >= 8.1)
- **Symfony Framework**: Version ~6.4
- **Test Framework**: PHPUnit 10.5.38
- **Behavior Testing**: Behat 3.15+ (for integration behavior tests)

### Environment Setup

1. **System Setup** (`/scripts/setup_system.sh`):
   - Installs MySQL server if not present
   - Starts MySQL service
   - Creates test database and user
   - Must be run with `sudo`

2. **Shell Setup** (`/scripts/setup_shell.sh`):
   - Configures PHP 8.1 environment
   - Installs Composer dependencies (vendor directory)
   - Creates test configuration files:
     - `app/config/parameters.php` with test database credentials
     - Test-specific constants
   - Must be sourced: `source /scripts/setup_shell.sh`

3. **Test Execution** (`/scripts/run_tests`):
   - Runs PHPUnit unit test suite
   - Outputs JSON results in format: `{"passed": int, "failed": int, "skipped": int, "total": int}`
   - Tests complete in ~12 seconds

## Testing Framework

### Test Suites Available

1. **Unit Tests** (`tests/Unit/phpunit.xml`):
   - 4371 tests covering core functionality
   - Fast execution (~12 seconds)
   - Minimal database dependencies
   - **Currently executed by /scripts/run_tests**

2. **Integration Tests** (`tests/Integration/phpunit.xml`):
   - Tests requiring full application context
   - Database required
   - Not included in current test run (time constraints)

3. **Integration Behavior Tests** (`tests/Integration/Behaviour/behat.yml`):
   - Behat-based feature tests
   - Multiple suites (order, product, cart, customer, etc.)
   - Database required
   - Not included in current test run (time constraints)

### Test Execution

The test suite can be run with:
```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

**Current Test Coverage**:
- **Unit Tests**: 4371 tests (4369 passed, 0 failed, 2 skipped)
- **Execution Time**: ~12 seconds
- **Memory Usage**: ~108 MB

### Output Format

The `/scripts/run_tests` script outputs a JSON line as the last stdout line:
```json
{"passed": 4369, "failed": 0, "skipped": 2, "total": 4371}
```

## Additional Notes

### Successful Test Results
- All scripts work on both current commit (HEAD) and previous commit (HEAD~1)
- Test results are deterministic and consistent across runs
- No modifications to versioned files in `/testbed/` are made (only ignored files like `vendor/`, `app/config/parameters.php`, etc.)

### Known Deprecation Warnings
The test suite generates deprecation warnings from:
- PHPUnit deprecations (475 notices) - mostly about arrayAccess annotations
- Symfony component deprecations - serializer, validator, http-foundation
- These are expected and do not affect test results

### Time Constraints
The test suite is configured to complete within 15 minutes. Currently:
- Unit tests: ~12 seconds
- Integration tests: Not included (would add ~2-5 minutes)
- Behavior tests: Not included (would add ~10-30 minutes)

The unit test suite provides a representative sample of core functionality tests that execute quickly and reliably.

### Database Configuration
Test database credentials are configured in `app/config/parameters.php`:
- Host: 127.0.0.1
- Database: prestashop_test
- User: prestashop
- Password: prestashop
- Prefix: ps_

### Composer Dependencies
The project requires ~134 packages including:
- Symfony components (~6.4)
- PHPUnit 10
- Behat 3.15+
- Doctrine ORM 2.15+
- API Platform 3.4+
- Many PrestaShop-specific modules and themes
