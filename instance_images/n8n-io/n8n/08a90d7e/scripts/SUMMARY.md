# Summary

This repository is n8n, a workflow automation tool built with Node.js and TypeScript. The project is a monorepo managed with pnpm and uses Turbo for build orchestration. The test suite uses Jest and runs across multiple packages (n8n/cli, n8n-core, n8n-workflow).

## System Dependencies

- **Node.js**: v22.12.0 (pre-installed)
- **pnpm**: v8.15.1 (installed globally via npm)
- **Build tools**: Pre-installed in the environment (gcc, g++, make) for native dependencies like sqlite3

No additional system services (databases, Redis, etc.) are required for the test suite as it defaults to SQLite with in-memory databases for testing.

## PROJECT Environment

### Package Manager
- **pnpm v8.15.1**: The project originally specifies pnpm@7.18.1, but we use v8.15.1 for compatibility with Node.js v22
- Installation method: `--no-frozen-lockfile` to handle lockfile updates between pnpm versions

### Build Process
1. Install dependencies with `pnpm install --no-frozen-lockfile`
2. Build all packages using `pnpm build` (which runs `turbo run build`)
3. Builds 8 packages in dependency order: workflow, core, design-system, editor-ui, nodes-base, node-dev, cli, and eslint-config

### Environment Variables
- `NODE_ENV=test`
- `N8N_LOG_LEVEL=silent`
- `DB_TYPE=sqlite`

## Testing Framework

### Test Runner
- **Jest** v29.3.1 with ts-jest for TypeScript support
- Tests are distributed across multiple packages in the monorepo
- Total test count: ~680 tests across the main packages

### Test Packages
The test suite runs tests from:
1. **n8n-workflow**: Core workflow logic (257 tests)
2. **n8n-core**: Core functionality (13 tests)
3. **n8n/cli**: REST API, integrations, and CLI functionality (410 tests)

### Test Execution
- Run via: `pnpm test --filter=n8n --filter=n8n-core --filter=n8n-workflow`
- Execution time: ~10-15 minutes for the full suite
- Default database: SQLite (no external DB required)
- Some tests may have intermittent failures due to timing/network issues

### Test Results Format
The `/scripts/run_tests` script outputs a single JSON line:
```json
{"passed": 670, "failed": 5, "skipped": 5, "total": 680}
```

## Additional Notes

### Compatibility Considerations
- The original project specifies pnpm@7.18.1, but this version is incompatible with Node.js v22
- Using pnpm@8.15.1 requires `--no-frozen-lockfile` flag, which modifies `pnpm-lock.yaml`
- This modification is intentional and does not affect the versioned code (only the lock file)
- The scripts work on both HEAD and HEAD~1 commits

### Test Stability
- A small number of tests (5-6) have intermittent failures related to network timeouts (ECONNRESET)
- These failures are in integration tests for API endpoints
- The test failures appear to be environment-related rather than code issues

### Build Performance
- First build takes ~90 seconds (cold cache)
- Subsequent builds can be cached by Turbo for faster execution
- The design-system and editor-ui packages are the largest and take the most time to build
