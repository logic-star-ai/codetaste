# Summary

This repository is a Node.js/TypeScript monorepo for the Nhost project, using pnpm as the package manager and Turbo for monorepo orchestration. The project contains multiple packages for authentication, storage, GraphQL, and framework integrations (React, Vue, Next.js).

## System Dependencies

- **Node.js**: Version 16.x (required by package.json: `"node": ">=16 <17"`)
- **pnpm**: Version 7.17.0 (specified in package.json)
- **NVM**: Used to switch between Node versions

No additional system services (databases, Redis, etc.) are required for running the tests.

## PROJECT Environment

### Package Manager
- **pnpm 7.17.0**: Workspace-enabled package manager for monorepo management
- **Turbo 1.6.3**: Build system for caching and parallel execution

### Key Technologies
- **TypeScript 4.9.4**: Primary language
- **Vitest 0.27.0**: Test framework with jsdom environment
- **Vite 4.0.2**: Build tool
- **React 18.2.0, Vue, Next.js**: Framework integrations

### Workspace Structure
The monorepo contains:
- **packages/**: Core packages (nhost-js, hasura-auth-js, hasura-storage-js, react, vue, nextjs, graphql-js, docgen)
- **integrations/**: Integration packages (apollo, stripe-graphql-js, google-translation, react-apollo, react-urql)
- **dashboard/**: Admin dashboard (excluded from test suite)
- **docs/**: Documentation (excluded from test suite)
- **examples/**: Example applications (excluded from test suite)

## Testing Framework

**Test Framework**: Vitest 0.27.0

### Configuration
- Tests use the `jsdom` environment for browser API simulation
- Configuration files located in `/testbed/config/`
- Test pattern: `**/*.{test,spec}.{ts,tsx}` in `src/` and `tests/` directories

### Test Execution
- Tests are run via `pnpm run test`, which uses Turbo to orchestrate test execution across all packages
- The `--threads=false` flag is required to avoid memory issues with Vitest's worker pool in the container environment
- JSON reporter is used for machine-readable output

### Test Coverage
As of the current commit, the test suite includes:
- **Total Tests**: 243 tests across all packages
- **Packages with Tests**:
  - @nhost/docgen: 59 tests
  - @nhost/hasura-auth-js: 131 tests
  - @nhost/nhost-js: 45 tests
  - @nhost/apollo: 1 test
  - @nhost/react: 1 test
  - @nhost/vue: 3 tests
  - @nhost/react-apollo: 1 test
  - @nhost/nextjs: 1 test
  - @nhost/react-urql: 1 test

## Additional Notes

### Memory Constraints
Vitest's default worker pool configuration causes "Out of memory: wasm memory" errors in the container environment. This is resolved by running tests with `--threads=false` to disable worker threads.

### Turbo Caching
Turbo caches test results, which speeds up subsequent runs. The test output parser handles both cached and fresh test runs.

### Build Dependencies
Tests depend on built packages (`pnpm run build` must complete before tests). The setup script automatically builds all packages if dist directories are missing.

### Excluded from Tests
The following are excluded from the test suite per package.json configuration:
- @nhost/dashboard
- @nhost/docs
- @nhost-examples/* (all example projects)
