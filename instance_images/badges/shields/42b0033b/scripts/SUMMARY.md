# Summary

This repository contains the Shields.io badge service - a Node.js application that generates SVG and raster format badges for GitHub READMEs and other web pages. The project uses JavaScript with ES modules and includes both server-side and frontend components.

## System Dependencies

- **Node.js**: Version 16.13.0 (required by package.json engines field)
- **npm**: Version 8.1.0 (comes with Node.js 16.13.0)
- **NVM**: Used to manage Node.js versions (located at /opt/nvm)

No additional system-level services (databases, Redis, etc.) are required for running the test suite.

## PROJECT Environment

The project uses the following setup:

1. **Runtime**: Node.js 16.13.0 installed via NVM at `/opt/nvm`
2. **Package Manager**: npm (version 8.1.0)
3. **Module System**: ES modules (type: "module" in package.json)
4. **Dependencies**: Installed via `npm ci` (2722 packages)
5. **Environment Variables**:
   - `NODE_ENV=test` - Sets Node environment
   - `NODE_CONFIG_ENV=test` - Sets config environment for the config library
6. **Pre-test Requirements**:
   - Service definitions must be generated: `npm run defs`
   - Supported features must be generated: `npm run features`

## Testing Framework

The project uses **Mocha** as its primary test framework with the following configuration:

- **Test Reporter**: `mocha-env-reporter` (configured in `.mocharc.yml`)
- **Frontend Tests**: Use `ts-mocha` with TypeScript support, Babel polyfill and register
- **Test Suites**:
  - `test:core` - Core functionality tests (lib, core, services)
  - `test:package` - Badge-maker package tests
  - `test:entrypoint` - Server entrypoint tests
  - `test:frontend` - Frontend React/TypeScript tests
  - `test:integration` - Integration tests (not run in standard test suite)

The `/scripts/run_tests` script runs a representative subset of tests covering:
- Core service logic
- Badge generation package
- Server entrypoint
- Frontend components

**Test Results** (HEAD commit c73072d):
- Passed: 1377 tests
- Failed: 0 tests
- Skipped: 0 tests
- Total: 1377 tests

**Test Results** (HEAD~1 commit 42b0033):
- Passed: 1379 tests
- Failed: 0 tests
- Skipped: 0 tests
- Total: 1379 tests

## Additional Notes

- The project has 143 npm audit vulnerabilities (20 low, 34 moderate, 71 high, 18 critical) which are known and do not affect test execution
- The test suite includes warnings about deprecated packages (@hapi/* packages) but these do not impact functionality
- The scripts are designed to be portable and work on both HEAD and HEAD~1 commits without modification
- The `git status` remains clean after running tests - all generated files (node_modules, frontend/service-definitions.yml, frontend/supported-features.json) are properly gitignored
- Test execution time is reasonable (~30-60 seconds for the complete suite)
- The environment requires no sudo access for shell setup or test execution, only for the system setup script (which does nothing in this case)
