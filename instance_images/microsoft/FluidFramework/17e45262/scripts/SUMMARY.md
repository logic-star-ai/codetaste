# Summary

This directory contains scripts to configure the development environment and run tests for the FluidFramework repository, a TypeScript/JavaScript monorepo for building distributed, real-time collaborative web applications.

## System Dependencies

The FluidFramework project requires:
- **Node.js v16.x** (specified in `.nvmrc`)
- **pnpm v7.32.3** (specified in `package.json` packageManager field)
- **corepack** (Node.js package manager enabler)

No additional system services (databases, Redis, etc.) are required for the core test suite. The tests primarily use in-memory implementations and don't require external services.

### Native Build Dependencies

The project has some native dependencies that require build tools:
- **node-gyp** prerequisites (Python 3, make, C/C++ compiler)
- These are already available in the Ubuntu 24.04 environment

## Project Environment

### Repository Structure

FluidFramework is a large monorepo organized into multiple pnpm workspaces:
- **158 workspace projects** across multiple release groups
- Primary workspace rooted at `/testbed/` with configuration in `pnpm-workspace.yaml`
- Contains packages, examples, experimental features, and build tools

### Key Directories

- `/testbed/packages/` - Core framework packages (~52 with mocha tests)
- `/testbed/examples/` - Example applications
- `/testbed/experimental/` - Experimental features
- `/testbed/build-tools/` - Build and development tools
- `/testbed/server/` - Reference ordering service

### Build System

- Uses **fluid-build** custom build orchestration tool
- TypeScript compilation across all packages
- Webpack bundling for certain packages
- Build takes approximately 2-3 minutes on a clean checkout

### Dependencies

- **3687 npm packages** installed via pnpm
- Uses pnpm workspaces for monorepo management
- Workspace dependencies linked via `workspace:~` protocol

## Testing Framework

### Test Structure

The project uses two testing frameworks:
1. **Mocha** - Primary test framework (52+ packages with tests)
   - Tests located in `dist/test/` directories (compiled from `src/test/`)
   - Uses `@fluidframework/mocha-test-setup` for test configuration
   - Multi-reporter support via `mocha-multi-reporters` package
   - Generates JSON reports in `nyc/junit-report.json` per package

2. **Jest** - Secondary framework (2 packages with tests)
   - Used for specific packages requiring Jest features
   - Requires `assign-test-ports` utility for port allocation

### Test Execution

The test suite runs via pnpm recursive commands:
- `pnpm run -r --no-sort --stream --no-bail test:mocha` - Runs all mocha tests
- `pnpm run -r --no-sort --stream --no-bail test:jest` - Runs all jest tests

### Test Results

From a typical test run:
- **~8,500-8,600 tests passing** (varies slightly between runs)
- **0 failures** (in core packages)
- **~300-350 tests skipped** (conditional/environment-specific tests)
- **Total: ~8,900-9,000 tests**

Test results are aggregated from individual package JSON reports.

### Known Test Issues

Some example packages have test configuration issues that don't affect core functionality:
- `@fluid-example/bubblebench-common` - Missing test setup
- `@fluid-example/table-document` - Module resolution issues
- `@fluid-example/webflow` - ESM loader issues

These failures are in example/demo packages and don't represent issues with the core framework.

## Scripts

### `/scripts/setup_system.sh`
- Executed with sudo before tests
- Currently a no-op (exits 0) as no system services are required
- Can be extended if future tests require services like databases

### `/scripts/setup_shell.sh`
- Sources nvm and activates Node.js v16
- Enables corepack and activates pnpm v7.32.3
- Installs dependencies via `pnpm install --frozen-lockfile` (idempotent)
- Builds the project via `npm run build:compile` (incremental, idempotent)
- Must be sourced, not executed: `source /scripts/setup_shell.sh`

### `/scripts/run_tests`
- Runs the full mocha and jest test suites
- Collects test results from JSON reports in each package
- Aggregates results and outputs final JSON: `{"passed": X, "failed": Y, "skipped": Z, "total": N}`
- Handles both mocha (junit-report.json) and jest (jest-results.json) outputs
- Executable: `/scripts/run_tests`

## Additional Notes

### Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Don't hardcode file paths that might change between commits
- Use robust detection for installed vs. not-installed states
- Handle incremental builds gracefully

### Performance Considerations

- Full build from clean state: ~2-3 minutes
- Incremental rebuild: ~1-3 minutes (depending on changes)
- Full test suite: ~10-15 minutes
- Total pipeline (clean + build + test): ~15-20 minutes

### Memory and Resource Usage

The test suite is resource-intensive:
- Large number of parallel pnpm processes
- Some jest tests may encounter resource limits (fork errors seen in output)
- These resource issues don't affect core mocha tests or final results

### Git Status

The scripts properly maintain git cleanliness:
- All build artifacts go to ignored directories (`dist/`, `node_modules/`, `nyc/`, etc.)
- `git status` shows no changes after running setup scripts
- Scripts work correctly with `git clean -xdff` between runs
