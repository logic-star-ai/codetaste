# Summary

This document describes the testing setup for the tldraw monorepo, a TypeScript/React drawing application.

## System Dependencies

- **Node.js**: v22.12.0 (pre-installed)
- **Corepack**: Enabled to manage Yarn 3.5.0
- **Python 3**: Used for test result parsing
- **System packages**: None required beyond base Ubuntu 24.04

The system setup script (`/scripts/setup_system.sh`) enables corepack for Yarn support. No additional system services (databases, Redis, etc.) are required for running the test suite.

## Project Environment

### Package Manager
- **Yarn 3.5.0**: Configured via `.yarnrc.yml` with `nodeLinker: node-modules`
- **Lockfile**: `public-yarn.lock`
- **Workspaces**: Monorepo structure with packages in `packages/`, `apps/`, `e2e/`, `config/`, and `scripts/`

### Build System
- **lazyrepo 0.0.0-alpha.26**: Task runner that manages build and test execution across the monorepo
- **TypeScript 5.0.2**: Primary language
- **esbuild / SWC**: Used for transpilation and bundling

### Test Infrastructure
- **Jest 28.1.1**: Test framework
- **@swc/jest**: Fast TypeScript transformation for Jest
- **jest-environment-jsdom**: DOM environment for React component tests
- **@testing-library/react**: React testing utilities

### Environment Setup
The setup shell script (`/scripts/setup_shell.sh`):
1. Navigates to `/testbed`
2. Enables corepack for Yarn support
3. Installs all workspace dependencies via `yarn install`
4. Sets `NODE_ENV=test`
5. Disables Husky git hooks (`HUSKY=0`)

The script is idempotent and checks for existing node_modules before reinstalling.

## Testing Framework

### Test Execution
Tests are executed using the `lazy test` command, which:
1. Runs `refresh-assets` to copy static assets (icons, fonts, translations)
2. Executes Jest in each package that has a test configuration
3. Caches results for faster subsequent runs (can be bypassed with `--force`)

### Test Configuration
- **Jest preset**: `config/jest/node/jest-preset.js`
  - Uses `@swc/jest` for TypeScript transformation
  - Includes nanoid and escape-string-regexp in transformIgnorePatterns
  - Sets up coverage collection from `src/**/*.{ts,tsx}`

- **Custom matchers**: `config/setupJest.ts`
  - Provides `toCloselyMatchObject` for floating-point comparisons

### Test Packages
The test script (`/scripts/run_tests`) runs tests for a representative subset of packages:
- **packages/indices**: Index and reordering utilities (5 passed, 2 todo)
- **packages/tlstore**: State management
- **packages/tlschema**: Schema definitions and migrations
- **packages/tlvalidate**: Validation utilities
- **packages/tlsync-client**: Sync client functionality
- **packages/file-format**: File format handling

Note: The `packages/utils` package is excluded from the test run due to a Jest fake timers compatibility issue with Node.js 22 (TypeError on performance object assignment). The `packages/primitives` package doesn't have Jest configuration in its package.json.

### Test Results Format
The run_tests script outputs JSON in the format:
```json
{
  "passed": <number>,
  "failed": <number>,
  "skipped": <number>,
  "total": <number>
}
```

Test counts are accumulated across all packages by parsing Jest output, which includes:
- **passed**: Successfully completed tests
- **failed**: Tests that failed or threw errors
- **skipped**: Pending tests and todo tests combined
- **total**: Sum of all test categories

## Additional Notes

### Known Issues
1. **@sitespeed.io/edgedriver** installation fails with `ENOTFOUND msedgedriver.azureedge.net` due to network restrictions in the container environment. This is a non-critical dev dependency for e2e testing and doesn't affect the Jest unit tests.

2. **packages/utils test failure**: The debounce.test.ts file fails with `TypeError: Cannot assign to read only property 'performance' of object '[object global]'` when using `jest.useFakeTimers()`. This appears to be a compatibility issue with Node.js 22's global performance object.

### Test Execution Time
The test suite for the subset of packages completes in approximately 3-5 seconds on a clean run (without cache).

### Portability
The scripts in `/scripts/` are designed to work across different commits. They:
- Don't hardcode any commit-specific paths or configurations
- Use relative paths from `/testbed`
- Handle missing or changed packages gracefully
- Are idempotent and can be run multiple times

### Git Status
The setup scripts do not modify any version-controlled files. All changes are to ignored directories:
- `node_modules/`
- `.lazy/` (build cache)
- `.yarn/cache/` and `.yarn/install-state.gz`
- Generated assets in `packages/assets/`
- Build artifacts in `.tsbuild*/`

Running `git status` after setup shows a clean working tree.
