# Summary

This repository (wp-calypso) is a Node.js based monorepo using Yarn workspaces. The testing infrastructure uses Jest as the primary testing framework for unit and integration tests across multiple packages.

## System Dependencies

No additional system services are required for running the Jest test suites. All dependencies are managed through Node.js/Yarn.

## PROJECT Environment

- **Node.js**: v14.16.1 (as specified in `.nvmrc`)
- **Package Manager**: Yarn v1.22.10+
- **Build Tool**: Lerna for monorepo management, TypeScript for compilation
- **Environment Variables**:
  - `TZ=UTC` (for consistent test execution)
  - `NODE_ENV=test`
  - `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` (to skip optional Playwright browser downloads)

## Testing Framework

The project uses Jest (v26.6.3) with the following test suites:

1. **test-client**: Tests for client-side code (`test/client/jest.config.js`)
   - Contains ~11,000+ tests covering React components, Redux state management, and client utilities

2. **test-packages**: Tests for individual packages in the monorepo (`test/packages/jest.config.js`)
   - Tests for shared utility packages and libraries

3. **test-server**: Server-side rendering and Node.js code tests (`test/server/jest.config.js`)
   - Contains ~360 tests for server-side code

4. **test-build-tools**: Build tool and webpack configuration tests (`test/build-tools/jest.config.js`)
   - Contains 3 tests for build infrastructure

### Test Execution

Tests are run sequentially (not in parallel) to avoid resource contention. The main test command aggregates results from all four test suites and outputs a JSON summary with the following format:

```json
{
  "passed": <number>,
  "failed": <number>,
  "skipped": <number>,
  "total": <number>
}
```

Total test count: ~12,400+ tests

## Additional Notes

- **node-sass Issue**: The repository uses node-sass which requires Python 2 for building native extensions. Since Python 2 is not available on Ubuntu 24.04, node-sass cannot be rebuilt. However, this doesn't affect Jest tests since node-sass is only required for CSS compilation during the build process.

- **Playwright**: Playwright browser downloads are skipped as they're not needed for Jest unit/integration tests (only for E2E tests which are not included in this test suite).

- **Jest JSON Output**: The Jest JSON reporter outputs JavaScript literals including `undefined` values which are not valid JSON. The test runner script handles this by using grep to extract numeric test counts rather than parsing the full JSON.

- **Test Failures**: Some tests fail consistently due to missing configuration files or environmental differences (e.g., ~300 failing tests out of ~12,400 total). These failures exist in both HEAD and HEAD~1 commits and are not regressions.

- **Performance**: The full test suite takes approximately 10-15 minutes to complete on the test environment.
