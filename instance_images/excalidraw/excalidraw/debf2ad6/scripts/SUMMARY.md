# Summary

This document describes the testing setup for the Excalidraw monorepo, a TypeScript/React-based project using Yarn workspaces for package management and Vitest for testing.

## System Dependencies

No system-level dependencies are required for this project. The setup scripts only require:
- Node.js v22.12.0 (compatible with the project's requirement of 18.0.0 - 22.x.x)
- npm (for installing yarn globally)
- Yarn v1.22.22 (installed globally via npm)
- jq (for JSON parsing in test scripts - pre-installed in environment)

## Project Environment

**Language**: TypeScript/JavaScript (Node.js)
**Package Manager**: Yarn v1.22.22 (specified in package.json as `packageManager: "yarn@1.22.22"`)
**Node Version**: 18 (from .nvmrc), compatible with v22.12.0 available in environment
**Project Type**: Yarn workspace monorepo with multiple packages:
  - excalidraw-app
  - packages/*
  - examples/*

**Key Dependencies**:
- React 19.0.10 and React DOM 19.0.4
- TypeScript 4.9.4
- Vitest 3.0.6 (testing framework)
- jsdom 22.1.0 (DOM environment for tests)
- @testing-library/react (component testing)
- vitest-canvas-mock (for canvas API mocking)

**Build Process**:
1. Install dependencies with `yarn install --frozen-lockfile`
2. Build packages with `yarn build:package` (builds packages/excalidraw)
3. Generate TypeScript types

## Testing Framework

**Framework**: Vitest v3.0.6
**Test Configuration**: vitest.config.mts
**Setup File**: setupTests.ts (configures test environment, mocks, and polyfills)
**Environment**: jsdom (simulates browser environment)
**Test Runner**: `yarn test:app --run` (non-watch mode)

**Test Structure**:
- Total test files: 85
- Total tests: 994
- Test locations:
  - excalidraw-app/tests/
  - packages/excalidraw/tests/
  - packages/*/tests/

**Test Results Format**:
Vitest outputs JSON format with the following structure:
```json
{
  "numTotalTests": 994,
  "numPassedTests": 909,
  "numFailedTests": 37,
  "numPendingTests": 47
}
```

**Current Test Results** (as of commit 1913599):
- Passed: 909
- Failed: 37
- Skipped: 47
- Total: 994

## Additional Notes

**Test Execution Time**: Full test suite runs in approximately 2-3 minutes on the environment.

**Build Warnings**: The project generates numerous peer dependency warnings during `yarn install`, which are expected and do not affect functionality. These include warnings about:
- @babel/* packages missing @babel/core peer dependency
- eslint plugins missing eslint peer dependency
- React-related packages with peer dependency warnings

**Git Status**: All scripts are designed to work without modifying versioned files in /testbed/. The `git status` command shows a clean working tree after test execution, confirming compliance with the requirement that only files ignored by version control (node_modules, dist, build artifacts) are modified.

**Portability**: The scripts are designed to work on both HEAD and HEAD~1 commits without modification, as verified during testing.

**Idempotency**: The setup_shell.sh script checks for existing installations and skips redundant work when dependencies are already installed, making it safe to run multiple times.
