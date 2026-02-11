# Summary

This repository is **Actual Budget**, a local-first personal finance tool written in Node.js/TypeScript. The project is organized as a Yarn 4 monorepo workspace containing multiple packages including the core logic (loot-core), API layer, web frontend (desktop-client), and desktop Electron app.

## System Dependencies

The project requires the following system-level dependencies:
- **Node.js**: v18.16.0 (as specified in `.nvmrc`)
- **Build tools**: gcc, g++, make, python3 (for compiling native dependencies like better-sqlite3)
- **NVM**: Node Version Manager for managing Node.js versions

No system services (databases, Redis, etc.) are required to run the test suite.

## PROJECT Environment

- **Package Manager**: Yarn v4.3.1 (Berry, installed via `.yarn/releases/yarn-4.3.1.cjs`)
- **Node Version**: v18.16.0 (managed via NVM)
- **Workspace Structure**: Yarn workspaces with packages:
  - `@actual-app/crdt` - CRDT layer for synchronization
  - `loot-core` - Core application logic
  - `@actual-app/api` - API layer for external integrations
  - `@actual-app/web` - Web frontend (React-based)
  - `desktop-electron` - Desktop Electron app wrapper
  - `eslint-plugin-actual` - Custom ESLint rules

- **Key Dependencies**:
  - better-sqlite3 (native dependency requiring build tools)
  - TypeScript, React, Redux Toolkit
  - Multiple test frameworks (Jest, Vitest, Playwright)

## Testing Framework

The project uses multiple testing frameworks across different packages:

1. **Jest** (v27.5.1):
   - Used for: `@actual-app/crdt`, `loot-core`, `@actual-app/api`
   - Configuration: Individual `jest.config.js` files in each package
   - Transform: `@swc/jest` for TypeScript compilation
   - Tests run with `--maxWorkers=1` to avoid resource exhaustion errors in constrained environments

2. **Vitest** (v1.6.0):
   - Used for: `@actual-app/web` (desktop-client)
   - Modern Vite-based test runner
   - Tests include React component tests with @testing-library/react

3. **Playwright** (v1.41.1):
   - Used for: E2E and VRT (Visual Regression Testing)
   - Not included in the standard test run due to time constraints

### Test Execution

Tests are run sequentially by workspace to avoid parallel execution issues:
1. CRDT tests (Jest): 20 tests
2. loot-core node tests (Jest): ~296 tests
3. API tests (Jest): 9 tests
4. Web tests (Vitest): ~123 tests

**Total**: ~448 tests covering core functionality, API operations, and frontend components.

### Test Output Format

The test runner outputs results in JSON format:
```json
{"passed": 445, "failed": 0, "skipped": 3, "total": 448}
```

## Additional Notes

### Challenges Encountered

1. **Resource Constraints**: Initial attempts to run tests in parallel (as configured in the project's default `yarn test` command) resulted in EAGAIN errors due to process/thread exhaustion. This was resolved by running tests with `--maxWorkers=1` for Jest and sequentially by workspace.

2. **Native Dependencies**: The better-sqlite3 package requires compilation during installation, necessitating build-essential tools (gcc, g++, make, python3). These are pre-installed in the environment.

3. **Multiple Test Frameworks**: The project uses both Jest and Vitest, requiring different approaches to JSON output parsing and result aggregation.

### Script Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification. The scripts:
- Use absolute paths where needed
- Detect if dependencies are already installed (idempotent)
- Don't modify versioned files (only install to node_modules and other ignored directories)
- Source NVM dynamically to ensure correct Node.js version

### Performance

The full test suite (excluding E2E/VRT tests) completes in approximately 1-2 minutes on a clean environment, including dependency installation time of ~25 seconds.
