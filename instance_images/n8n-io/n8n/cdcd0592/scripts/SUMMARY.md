# Summary

This repository contains n8n, a workflow automation platform. The testing setup is configured to run a representative subset of the backend test suite using Jest as the testing framework within a pnpm monorepo structure managed by Turbo.

## System Dependencies

- **Node.js**: v22.12.0 (requires >=20.15 as specified in package.json)
- **pnpm**: v10.2.1 (package manager, installed globally via npm)
- **jq**: For JSON parsing of test results (pre-installed in the environment)
- **git**: For repository management

No additional system services are required for the default SQLite-based test suite. The tests use SQLite as the database backend which requires no separate server installation.

## Project Environment

### Package Manager
- **pnpm v10.2.1**: Used for dependency management with workspace support
- Configuration in `.npmrc` includes workspace-specific settings like `prefer-workspace-packages=true`

### Build System
- **Turbo v2.3.3**: Monorepo task runner for managing builds and tests across 34 workspace packages
- **TypeScript v5.8.2**: For transpilation with strict type checking
- Builds are cached by Turbo to improve performance on subsequent runs

### Environment Variables
The following environment variables are set for testing:
- `NODE_ENV=test`
- `N8N_LOG_LEVEL=silent` - Suppresses log output during tests
- `DB_TYPE=sqlite` - Uses SQLite for database operations
- `CI=false` - Disables CI-specific behaviors
- `COVERAGE_ENABLED=false` - Disables coverage collection for faster test execution

### Monorepo Structure
The project consists of 34 packages organized in:
- `packages/@n8n/*` - Core n8n packages (23 packages)
- `packages/cli` - CLI interface (n8n package)
- `packages/core` - Core functionality
- `packages/workflow` - Workflow engine
- `packages/nodes-base` - Base node implementations
- `packages/frontend/*` - Frontend packages

## Testing Framework

### Test Runner
- **Jest v29.6.2**: Primary test framework
- **ts-jest v29.1.1**: TypeScript support for Jest
- Configuration in `jest.config.js` at the root and individual packages

### Test Execution
The `/scripts/run_tests` script executes tests for a representative subset of packages:
1. **@n8n/decorators** - Decorator utilities tests
2. **@n8n/di** - Dependency injection tests
3. **@n8n/config** - Configuration management tests
4. **@n8n/api-types** - API type validation tests
5. **@n8n/client-oauth2** - OAuth client tests
6. **@n8n/permissions** - Permission system tests (includes new tests from HEAD)
7. **n8n-workflow** - Workflow engine tests (largest test suite with 1160+ tests)
8. **n8n-core** - Core functionality tests

This subset provides good coverage of the backend stack while completing within the 15-minute time limit.

### Test Results Format
Tests output results in the following JSON format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

Results are aggregated from multiple test runs by parsing Jest's output format.

### Test Execution Time
- Full representative subset: ~60 seconds
- Total test count: 2664 tests (on HEAD)
- All tests passing in current implementation

## Additional Notes

### Build Process
- The initial setup requires a full build of all packages which takes approximately 2-3 minutes
- Subsequent builds are faster due to Turbo's caching mechanism
- The build process generates a `schema.json` file in `@n8n/extension-sdk` that is automatically restored to prevent git status changes

### Portability
All scripts have been tested on both HEAD (2bb1903) and HEAD~1 (cdcd059) to ensure compatibility across commits. The test count differs slightly between commits (2664 on HEAD vs 2600 on HEAD~1) due to new tests added in the HEAD commit.

### Setup Scripts
1. **`/scripts/setup_system.sh`**: No-op script (no system services required for SQLite tests)
2. **`/scripts/setup_shell.sh`**: Installs dependencies with pnpm and builds all packages
3. **`/scripts/run_tests`**: Runs the test suite and outputs JSON results

### Known Behaviors
- Jest workers may report EPIPE errors when checking memory usage - these are non-fatal and don't affect test results
- Some TypeScript compilation warnings appear during build (e.g., unused slot conditions) but don't prevent successful compilation
- The schema.json file is auto-generated during build and is restored by setup_shell.sh to maintain clean git status
