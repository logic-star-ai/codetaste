# Summary

This repository contains PrestaShop, an open-source e-commerce platform written in PHP. The testing setup has been configured to run PHPUnit unit tests with proper database and environment configuration.

## System Dependencies

The following system packages are installed via `setup_system.sh`:

- **PHP 8.1** with required extensions:
  - php8.1-cli, php8.1-common
  - php8.1-curl, php8.1-dom, php8.1-gd
  - php8.1-intl, php8.1-mbstring, php8.1-mysql
  - php8.1-xml, php8.1-zip
  - php8.1-bcmath, php8.1-soap
- **MySQL Server** (mysql-server, mysql-client)
- **Composer** (installed globally to /usr/local/bin)
- **unzip** (for extracting PHP packages)

The PHP repository from ppa:ondrej/php is added to get PHP 8.1 on Ubuntu 24.04.

## Project Environment

The shell environment is configured via `setup_shell.sh`:

1. **Database Configuration**:
   - Creates `app/config/parameters.php` with database connection settings
   - Database: test_prestashop (created automatically)
   - User: root (no password)
   - Prefix: ps_

2. **PHP Dependencies**:
   - Installs all dependencies via Composer (includes PHPUnit and other testing tools)
   - Timeout set to 600 seconds for slow package downloads

3. **Test Database**:
   - Creates test database with utf8mb4 character set
   - Initializes database schema using `tests/bin/create-test-db.php`
   - Database initialization is skipped if tables already exist

4. **Cache Directories**:
   - Creates var/cache/test, app/logs, var/cache/dev, var/cache/prod
   - Clears test cache before running tests

## Testing Framework

- **Framework**: PHPUnit 10
- **Test Suite**: Unit tests only (for faster execution)
- **Configuration**: tests/Unit/phpunit.xml
- **Test Count**: ~16,400 tests
- **Execution Time**: ~2-3 minutes for unit tests
- **Output Format**: JSON with passed/failed/skipped/total counts

The `run_tests` script:
- Runs PHPUnit with JUnit XML logging
- Parses the XML output to extract test counts
- Outputs results in JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Git Status
The scripts are designed to not modify any versioned files. All changes are made to ignored files/directories:
- app/config/parameters.php (generated, not in git)
- vendor/ (Composer packages, ignored)
- modules/* (downloaded modules, ignored)
- var/cache/* (cache directories, ignored)
- app/logs/* (log directories, ignored)

After running tests, `git status` should show no changes to versioned files.

### Portability
The scripts work on both HEAD and HEAD~1 commits without modifications, as required. They dynamically adapt to the repository state.

### Performance Optimizations
- Database initialization is skipped if tables already exist (idempotent setup)
- Composer installation is skipped if vendor/phpunit already exists
- Only unit tests are run (not integration tests) to keep execution time under 15 minutes

### Known Issues
None encountered. The setup successfully:
- Installs all system dependencies
- Configures PHP 8.1 environment
- Sets up MySQL database
- Runs 16,429 tests with 8 skipped, 0 failures
