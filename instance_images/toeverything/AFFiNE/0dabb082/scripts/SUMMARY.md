# Summary

This document describes the testing setup for the AFFiNE project, a TypeScript/JavaScript monorepo with Rust components.

## System Dependencies

No system-level services are required for running the test suite. The tests run entirely within the development environment using:
- Node.js v20.x runtime (managed via NVM)
- Yarn v4.1.0 package manager (enabled via corepack)
- Rust 1.76.0 toolchain (for native modules, though not required for current test suite)

All necessary system dependencies are pre-installed in the environment.

## PROJECT Environment

### Language & Runtime
- **Primary Language**: TypeScript/JavaScript
- **Node.js Version**: 20.x (as specified in `.nvmrc`)
- **Package Manager**: Yarn 4.1.0 (Berry)
- **Rust Toolchain**: 1.76.0 (as specified in `rust-toolchain.toml`)

### Project Structure
- **Type**: Monorepo using Yarn workspaces
- **Key Directories**:
  - `packages/common/`: Shared common packages
  - `packages/frontend/`: Frontend packages including core, components, etc.
  - `packages/backend/`: Backend server packages
  - `packages/frontend/electron/`: Electron desktop application (tests excluded from suite)

### Environment Setup
The setup involves three scripts:

1. **`/scripts/setup_system.sh`**: Executed with sudo, performs runtime system configuration. Currently no services are needed, so it's a no-op that exits successfully.

2. **`/scripts/setup_shell.sh`**: Sourced to configure the shell environment:
   - Loads NVM and switches to Node.js 20.x
   - Enables corepack for Yarn support
   - Installs project dependencies if needed (idempotent)
   - Sets environment variables (NODE_ENV=test, CI=true)
   - Configures Rust toolchain path

3. **`/scripts/run_tests`**: Executes the test suite:
   - Temporarily disables workspace configuration to exclude electron tests
   - Runs vitest in non-watch mode
   - Parses output and generates JSON results

### Dependencies Installation
Dependencies are installed automatically by `/scripts/setup_shell.sh` using:
```bash
yarn install
```

The installation is idempotent and skips if dependencies are already present.

## Testing Framework

### Test Runner
- **Framework**: Vitest 1.3.1
- **Configuration**: `vitest.config.ts` (root configuration)
- **Test Pattern**: `packages/{common,frontend}/**/*.spec.{ts,tsx}`
- **Excluded**: `packages/frontend/electron` (requires native Rust modules)

### Test Execution
Tests are run using the command:
```bash
yarn vitest --run
```

The workspace configuration (`vitest.workspace.ts`) is temporarily disabled during test execution to exclude electron tests which require building native Rust modules.

### Test Results
The test suite outputs results in JSON format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

### Test Coverage
- **Test Files**: ~29-31 test files
- **Total Tests**: ~95-97 tests (varies between commits)
- **Test Types**: Unit tests for:
  - Common utilities (debug, environment, data structures)
  - Frontend components (UI components, hooks, page lists)
  - Workspace implementations (local sync, storage adapters)
  - Infrastructure (DI, lifecycle, live data)

## Additional Notes

### Electron Tests Exclusion
The electron package tests (`packages/frontend/electron/test/**`) are excluded from the test suite because they require:
1. Native Rust modules to be built (`@affine/native-linux-x64-gnu`)
2. The native module build process using `napi-rs`

These tests would require additional build time (5-10 minutes) and are not representative of the core functionality being tested.

### Workspace Configuration
The project uses a vitest workspace configuration (`vitest.workspace.ts`) that includes both the root and electron projects. To run only the non-electron tests, the workspace file is temporarily renamed during test execution.

### Script Portability
All scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Don't hardcode file paths that might change
- Use configuration files that are part of the repository
- Handle missing or changed dependencies gracefully

### Performance
- **Setup Time**: ~30-50 seconds (dependency installation)
- **Test Execution**: ~10-15 seconds
- **Total Time**: ~40-60 seconds for a complete clean test run

### Known Issues
None encountered during testing setup.
