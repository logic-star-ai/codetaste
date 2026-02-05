# Summary

This repository contains **html-react-parser**, a TypeScript/JavaScript library that converts HTML strings to React elements. The project uses Jest for testing with TypeScript support via ts-jest.

## System Dependencies

No system-level services or runtime dependencies are required for this project. The `/scripts/setup_system.sh` script exits cleanly without performing any operations.

## PROJECT Environment

- **Language**: TypeScript/JavaScript (Node.js)
- **Node.js Version**: 20 (specified in `.nvmrc`)
- **Package Manager**: npm (uses `npm ci --ignore-scripts` for reproducible installs)
- **Key Dependencies**:
  - React 18.2.0 (peer dependency)
  - TypeScript 5.2.2
  - Jest 29.7.0
  - ts-jest 29.1.1

### Environment Setup

The `/scripts/setup_shell.sh` script:
1. Changes to the `/testbed` directory
2. Loads nvm and switches to Node.js version 20
3. Installs npm dependencies via `npm ci --ignore-scripts` (skipping husky git hooks which are unnecessary for testing)
4. Sets `CI=true` environment variable for test execution

## Testing Framework

**Test Framework**: Jest 29.7.0 with ts-jest preset

**Test Configuration** (`jest.config.ts`):
- Preset: `ts-jest`
- Coverage collection enabled with 100% thresholds for all metrics
- Tests exclude integration tests by default (via `--testPathIgnorePatterns test/integration`)

**Test Execution**:
- Command: `npx jest --testPathIgnorePatterns test/integration --json --ci --colors`
- Test files: Located in `/testbed/test/` directory
  - `attributes-to-props.test.ts`
  - `dom-to-react.test.tsx`
  - `index.test.tsx`
  - `utilities.test.ts`
- Integration tests are excluded from the standard test run
- ESM tests are also excluded from the main test suite

**Test Results**:
- HEAD (4255a10): 115 tests pass (0 failed, 0 skipped)
- HEAD~1 (1fcb059): 113 tests pass (0 failed, 0 skipped)

The `/scripts/run_tests` script outputs JSON in the required format:
```json
{"passed": 115, "failed": 0, "skipped": 0, "total": 115}
```

## Additional Notes

- The project uses `npm ci --ignore-scripts` to skip postinstall hooks (husky) that would normally set up git commit hooks, as these are not needed for test execution
- Git status remains clean after running the setup scripts - all modifications are to ignored directories (`node_modules`, `coverage`, etc.)
- The scripts are portable and work on both HEAD and HEAD~1 commits without modification
- Test output is redirected to stderr (via `2>/dev/null` for jest's console output) to ensure only the JSON result appears on stdout
- The slight difference in test count between commits (115 vs 113) reflects the TypeScript migration that occurred in the HEAD commit
