# Summary

This repository contains the Elastic UI (EUI) component library, a React-based UI framework for building Elastic applications. The testing infrastructure is configured to run Jest-based unit tests across the component library.

## System Dependencies

No system-level dependencies or services are required for running the test suite. All necessary packages are managed through npm/yarn.

The testing environment requires:
- Node.js 16.18.1 (managed via NVM)
- Yarn 1.22.19 (package manager)

## PROJECT Environment

The project is a Node.js/TypeScript application with the following key characteristics:

- **Language**: TypeScript/JavaScript (React components)
- **Runtime**: Node.js 16.18.1 (specified in `.nvmrc`)
- **Package Manager**: Yarn (with frozen lockfile)
- **Build System**: Webpack with Babel transpilation
- **Dependencies**: Installed via `yarn install --frozen-lockfile`

### Environment Variables

The following environment variables are set during testing:
- `NODE_ENV=test`: Ensures test-specific configurations are used
- `CI=true`: Activates CI-specific behaviors in test runners

### Runtime Configuration

- NVM is used to switch to Node 16.18.1 from the system default (22.12.0)
- NVM is located at `/opt/nvm/`
- Yarn is installed globally per Node version
- Dependencies are cached in `node_modules/` to avoid redundant installations

## Testing Framework

The project uses **Jest** as its primary testing framework with the following configuration:

- **Test Command**: `yarn test-unit` (runs `jest --config ./scripts/jest/config.json`)
- **Test Files**: Matches `**/*.test.js`, `**/*.test.ts`, `**/*.test.tsx`
- **Test Locations**:
  - `src/` (main component tests)
  - `src-docs/src/components` (documentation component tests)
  - `scripts/babel` (build tool tests)
  - `scripts/tests` (test infrastructure tests)
  - `packages/eslint-plugin` (linter plugin tests)

### Test Configuration

- **Enzyme**: Used for React component testing (configured with React 17 adapter)
- **Coverage**: Collected from `src/{components,services,global_styling}/**/*.{ts,tsx,js,jsx}`
- **Snapshots**: 2976 snapshot tests
- **Mock Setup**: File and style imports are mocked
- **Test Timeout**: 30 seconds per test

### Test Output

The test suite produces JSON output with the following structure:
```json
{
  "passed": 4588,
  "failed": 0,
  "skipped": 10,
  "total": 4598
}
```

### Test Suite Statistics (HEAD commit)

- **Total Tests**: 4,598
- **Test Suites**: 377 (376 passed, 1 skipped)
- **Passed**: 4,588
- **Skipped**: 10
- **Failed**: 0
- **Execution Time**: ~90-95 seconds

## Additional Notes

### Node Version Management

The repository specifies Node 16.18.1 in `.nvmrc`, but the pre-installed system has Node 22.12.0. NVM is successfully used to switch to the correct version. The setup scripts automatically detect NVM at `/opt/nvm/` and switch versions accordingly.

### Yarn Installation

Yarn must be installed globally for each Node version managed by NVM. The setup script handles this automatically, checking for yarn availability and installing it if needed.

### Test Stability

The test suite is deterministic and produces consistent results across runs. There are warnings about potential memory leaks (MaxListenersExceededWarning) and Jest not exiting immediately after test completion, but these do not affect test results or exit codes.

### Git Cleanliness

All dependency installations and build artifacts are written to ignored directories (`node_modules/`, build caches). Running the test suite does not modify any version-controlled files, ensuring `git status` remains clean.

### Portability

The scripts are designed to work across commits. Testing on both HEAD (1b82dd8) and HEAD~1 (b2893e2) confirmed compatibility, with expected minor variations in test counts due to code changes between commits.
