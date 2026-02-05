# Summary

This document describes the test environment configuration for the n8n-monorepo project, a workflow automation tool built with Node.js/TypeScript.

## System Dependencies

The n8n-monorepo project has minimal system dependencies:

- **Node.js**: v22.12.0 (pre-installed, required version: >=20.15)
- **pnpm**: v9.6.0 (installed globally via npm during setup)
- **SQLite**: Used for test database (no server required, native bindings compiled during pnpm install)

No additional system services (databases, Redis, etc.) are required for running the test suite, as SQLite is used for all database tests.

## Project Environment

The project is a **pnpm monorepo** with the following structure:

- **Package Manager**: pnpm v9.6.0 (specified in package.json)
- **Build System**: Turbo (turborepo) for managing the monorepo build and test tasks
- **Test Framework**: Jest for backend tests (with ts-jest for TypeScript support)
- **Additional Frontend Tests**: Vitest for packages/design-system and packages/editor-ui

### Key Packages Tested

The `test:backend` command runs tests for the following packages:
- `@n8n/api-types` (21 tests)
- `@n8n/client-oauth2` (18 tests)
- `@n8n/config` (4 tests)
- `@n8n/imap` (11 tests)
- `@n8n/permissions` (11 tests)
- `n8n-workflow` (945 tests)
- `n8n-core` (325 tests)
- `n8n` (main CLI package - 2021 tests)

Total: **3356 tests** in the backend test suite

### Build Requirements

The project requires a full build before tests can run. The build process:
1. Compiles TypeScript for all packages in dependency order
2. Uses turbo to parallelize builds where possible
3. Takes approximately 60 seconds on first build
4. Cached builds are much faster (< 10 seconds)

## Testing Framework

### Test Execution

Tests are executed using:
```bash
pnpm test:backend
```

This command runs `turbo run test:backend --concurrency=1`, which:
- Runs Jest test suites in each package
- Uses concurrency=1 to avoid database conflicts
- Uses SQLite as the test database (DB_TYPE=sqlite)
- Sets N8N_LOG_LEVEL=silent to reduce noise

### Test Configuration

- **Configuration Files**:
  - Root `jest.config.js` provides base configuration
  - Individual packages may have their own jest.config.js
- **Environment Variables**:
  - `NODE_ENV=test`
  - `N8N_LOG_LEVEL=silent`
  - `DB_TYPE=sqlite`
- **Test Pattern**: `\.(test|spec)\.(js|ts)$`

### Test Output Format

The `/scripts/run_tests` script parses the turbo/jest output and produces a single JSON line:
```json
{"passed": 3356, "failed": 0, "skipped": 0, "total": 3356}
```

## Additional Notes

### Script Portability

All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work with both the current commit (HEAD) and the previous commit (HEAD~1), as verified during setup.

### Performance Considerations

- First-time setup (clean environment) takes approximately 60-90 seconds
- Subsequent runs with cached builds take approximately 20-30 seconds
- The build step is conditionally executed in `setup_shell.sh` to avoid unnecessary rebuilds

### Idempotency

The `setup_shell.sh` script is idempotent and can be sourced multiple times without issues. It checks for:
- Existing node_modules
- Built packages (dist directories)
- Timestamp comparison of pnpm-lock.yaml vs node_modules

### No System Modifications

As required, `/scripts/setup_shell.sh` only modifies files that are ignored by git (node_modules, dist directories, .turbo cache). The git working tree remains clean after setup and testing.
