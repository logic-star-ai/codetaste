# Summary

This document describes the testing setup for the Monkeytype project, a Node.js-based monorepo using pnpm workspaces and turbo for task orchestration.

## System Dependencies

No additional system dependencies are required beyond the pre-installed environment. The project uses:
- **Node.js v20.16.0** (installed via nvm)
- **pnpm v9.6.0** (installed via npm)
- All test infrastructure is self-contained within the node_modules

The backend tests use:
- **vitest-mongodb**: In-memory MongoDB mock (downloads MongoDB binaries automatically)
- **ioredis-mock**: In-memory Redis mock

No external database services or system daemons need to be running.

## Project Environment

**Language**: TypeScript/JavaScript (Node.js)

**Package Manager**: pnpm v9.6.0 with workspaces

**Monorepo Structure**:
- `packages/util` - Utility functions package
- `packages/contracts` - Shared contracts and schemas
- `backend` - Backend API service
- `frontend` - Frontend application
- Additional configuration packages

**Build System**: Turbo for monorepo task orchestration

**Key Setup Steps**:
1. Install Node.js 20.16.0 via nvm
2. Install pnpm v9.6.0 globally
3. Install all workspace dependencies with `pnpm install --frozen-lockfile`
4. Build workspace packages (`packages/util` and `packages/contracts`) that are dependencies for backend and frontend
5. Tests can then run in each workspace independently

## Testing Framework

**Framework**: Vitest v2.0.5

**Configuration**:
- Each workspace has its own vitest configuration
- Backend uses `pool: 'forks'` with global setup for MongoDB mock
- Frontend uses happy-dom as the test environment
- Tests are run with `--pool.threads.singleThread=true` to avoid resource exhaustion

**Test Execution**:
- Tests are run sequentially by workspace to avoid thread/resource limits
- Total test count: ~768 tests (766 passed, 2 failed in HEAD)
- Test packages: `packages/util`, `packages/contracts`, `backend`, `frontend`

**Test Output Parsing**:
- Vitest outputs summary lines in format: `Tests  X passed (Y)`
- The run_tests script aggregates results across all workspaces
- Final output format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Environment Constraints
- The container environment has limited thread resources, so tests must run with minimal parallelism
- Using `--pool.threads.singleThread=true` prevents pthread_create errors
- Turbo concurrency is not explicitly limited as we run vitest sequentially per package

### Build Requirements
- Workspace packages (`@monkeytype/util`, `@monkeytype/contracts`) must be built before running tests
- The frontend and backend tests import from these packages
- Build is performed once during setup and cached with a marker file

### Test Failures
- 2 tests consistently fail in `frontend/__tests__/elements/test-activity-calendar.spec.ts`
- These appear to be legitimate test failures (not infrastructure issues)
- All other tests (766/768) pass successfully

### Script Portability
- All scripts work on both HEAD and HEAD~1 without modification
- The setup handles differences in workspace structure between commits
- Marker files (`.pnpm_install_marker`, `.build_marker`) enable idempotent execution
