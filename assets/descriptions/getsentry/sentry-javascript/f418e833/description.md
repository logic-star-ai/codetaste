# Migrate Node Integration Tests from Jest to Vitest

## Summary
Migrate all node integration tests from Jest to Vitest, converting callback-based tests to async/await pattern.

## Why
Vitest doesn't support the `done` callback pattern used extensively in Node integration tests with Jest. This migration aligns with the monorepo's testing infrastructure modernization.

## What Changed

### Test Runner & Server
- `runner.start(done)` → `await runner.start().completed()`
- `createTestServer(done)` → async pattern with `await createTestServer().start()`
- Test server `close()` now throws errors instead of passing to callback

### Test Files
- Import from `vitest` instead of Jest globals
- Convert all callback-based tests (`test('...', done => {...})`) to async (`test('...', async () => {...})`)
- Replace `done()` calls with `await runner.completed()`
- Replace `setTimeout(() => { ...; done(); })` with `await new Promise(resolve => setTimeout(resolve, ...))`

### Configuration
- Remove `jest.config.js`, `jest.setup.js`
- Add `vite.config.ts` for Vitest
- Update `package.json` test scripts
- Set test timeouts via `{ timeout: X }` option instead of `jest.setTimeout()`

### Cleanup
- Remove `afterEach(() => cleanupChildProcesses())` (now in Vitest setup)
- Consolidate test expectations to use Vitest's `expect`

## Scope
~300+ test files across all integration test suites including:
- Express (v4 & v5)
- Tracing (various integrations)
- Public API tests
- ANR, sessions, ESM tests
- Database integrations (MongoDB, PostgreSQL, MySQL, etc.)
- ... and more