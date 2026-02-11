# Summary

This repository is **wp-calypso**, a JavaScript/Node.js project that is the REST-API and JS-based version of the WordPress.com admin. The test environment has been successfully configured to run Jest-based tests across multiple test suites.

## System Dependencies

No system-level dependencies are required beyond Node.js. The project uses:
- **Node.js**: Version 22.9.0 (specified in `.nvmrc`, but runtime uses v22.12.0 which is compatible)
- **Yarn**: Version 4.0.2 (uses Corepack)
- **Package Manager**: Yarn v4 with workspaces (monorepo structure)

## Project Environment

The project is configured as follows:

### Runtime
- **Primary Language**: JavaScript/TypeScript (Node.js)
- **Package Manager**: Yarn 4.0.2 (Berry) with node_modules linker
- **Monorepo**: Yes, using Yarn workspaces with packages in `client/`, `desktop/`, `apps/*`, `packages/*`, and `test/e2e`

### Dependencies
- All dependencies are installed via `yarn install --immutable`
- Total installation time: ~2-3 minutes on first run
- Cached installations are significantly faster

### Environment Variables
- `NODE_ENV=test`
- `TZ=UTC` (ensures consistent timezone for test execution)
- `CI=true`
- `NO_COLOR=1` (for easier test output parsing)

## Testing Framework

**Framework**: Jest v29.6.1

### Test Structure
The project has multiple test suites organized by domain:
1. **test-packages**: Tests for packages in the `packages/` directory (214 test suites, ~2975 tests)
2. **test-server**: Server-side tests in `client/server/` (14 test suites, ~355 tests)
3. **test-build-tools**: Build tools tests (smaller suite)
4. **test-client**: Client tests (not included in current run to keep within 15-minute limit)

### Test Execution
- **Command**: `yarn test` (runs all test suites) or individual commands like `yarn test-packages`
- **Representative Subset**: The `/scripts/run_tests` script runs `test-packages`, `test-server`, and `test-build-tools` as a representative subset
- **Execution Time**: ~2-5 minutes for the subset
- **Parallel Execution**: Tests run with `--maxWorkers=4` for optimal performance

### Test Results
From the current HEAD:
- **Total Tests**: ~3330
- **Passed**: ~3324
- **Failed**: 4 (known failures in `client/server/lib/logger/test/index.js`)
- **Skipped**: 2

### Output Format
The test runner outputs results in the format:
```
{"passed": <number>, "failed": <number>, "skipped": <number>, "total": <number>}
```

## Additional Notes

### Notable Configuration
- The project uses babel, webpack, and various build tools
- Some tests use React Testing Library and jsdom for DOM testing
- E2E tests use Playwright (in `test/e2e/`) but are not included in the representative test run

### Potential Issues Encountered
1. **Browserslist warnings**: The codebase data is 8 months old, causing numerous warnings during test runs. These are filtered from stderr to reduce noise.
2. **Mock-fs failures**: Some tests in `client/server/lib/logger/test/index.js` fail due to mock-fs conflicts (4 test failures).
3. **Deprecation warnings**: Various React and Node.js deprecation warnings appear but don't affect test execution.

### Portability
The scripts (`/scripts/setup_system.sh`, `/scripts/setup_shell.sh`, and `/scripts/run_tests`) are designed to work on both HEAD and HEAD~1 commits without modification, ensuring compatibility across recent changes in the repository.
