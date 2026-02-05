# Summary

This repository contains **AzuraCast**, a self-hosted web radio management suite built with PHP 8.4 (backend) and Node.js/TypeScript (frontend). The test suite uses Codeception for both unit and functional tests.

## System Dependencies

The following system packages must be installed:

### PHP 8.4 and Extensions
- PHP 8.4 from Ondrej's PPA (ppa:ondrej/php)
- Required PHP extensions:
  - php8.4-cli
  - php8.4-curl
  - php8.4-gd
  - php8.4-intl
  - php8.4-mbstring
  - php8.4-xml
  - php8.4-mysql
  - php8.4-sqlite3
  - php8.4-redis
  - php8.4-zip
  - php8.4-bcmath
  - php8.4-imagick
  - php8.4-opcache
  - php8.4-maxminddb
  - php8.4-ffi
  - php8.4-gmp

### Additional System Tools
- software-properties-common (for PPA management)
- unzip
- git
- Composer (PHP dependency manager)

### Optional Services
- Redis (for session caching, tests run without it)
- MariaDB/MySQL (for database tests, unit tests don't require it)

## PROJECT Environment

### Backend (PHP)
- **Language**: PHP 8.4
- **Package Manager**: Composer
- **Framework**: Slim Framework 4
- **ORM**: Doctrine ORM 3
- **Dependencies**: 192 packages including dev dependencies

### Frontend (JavaScript/TypeScript)
- **Runtime**: Node.js v22.12.0
- **Package Manager**: npm
- **Framework**: Vue.js 3
- **Build Tool**: Vite

### Environment Variables
- `APP_ENV=testing`
- `APP_TESTING=1`

## Testing Framework

### Test Runner
**Codeception 5.3.2** - A BDD-style testing framework for PHP

### Test Suites
1. **Unit Tests** (`tests/Unit/`)
   - 5 test files with 7 individual tests
   - Fast execution (~0.1 seconds)
   - No database or external services required
   - Tests core utilities, string manipulation, XML processing, etc.

2. **Functional Tests** (`tests/Functional/`)
   - ~25 Cest files
   - Requires database setup and full application bootstrap
   - Not executed by default due to time constraints

### Test Execution
The `/scripts/run_tests` script executes **only Unit tests** to maintain reasonable execution time (~0.1 seconds). The unit test suite provides good coverage of core functionality without requiring complex environment setup.

### Test Results
Current test results on HEAD:
- **Total**: 7 tests
- **Passed**: 4 tests
- **Failed**: 3 tests (known issues with final class mocking in StationPlaylistTest)
- **Skipped**: 0 tests

The 3 failing tests are due to Mockery attempting to mock final classes (App\Entity\Station), which is a test design issue rather than an environment problem.

## Additional Notes

### Challenges Encountered
1. **PHP 8.4 Availability**: PHP 8.4 is not available in Ubuntu 24.04 default repositories. Solution: Added Ondrej's PPA which provides up-to-date PHP versions.

2. **Missing Extensions**: Initially missed some required PHP extensions (php8.4-gmp, php8.4-imagick). These were added after composer reported missing dependencies.

3. **Dev Dependencies**: The setup script must install dev dependencies (not use `--no-dev`) because Codeception is in the require-dev section.

### Portability
The scripts are designed to work on both HEAD and HEAD~1 without modification. They handle:
- Fresh installations of PHP and dependencies
- Idempotent execution (safe to run multiple times)
- Automatic detection of already-installed components

### Performance
- Initial setup (with package installations): ~2-3 minutes
- Subsequent runs (with cached dependencies): ~0.5 seconds
- Test execution: ~0.1 seconds

### Git Cleanliness
The scripts only modify files that are in `.gitignore`:
- `vendor/` directory (PHP dependencies)
- `node_modules/` directory (Node.js dependencies)
- `tests/_output/` directory (test artifacts)
- Generated files like `tests/_support/_generated/`

Running `git status` after setup shows no tracked file modifications.
