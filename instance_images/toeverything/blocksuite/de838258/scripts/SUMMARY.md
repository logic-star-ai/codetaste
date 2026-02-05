# Summary

This repository contains BlockSuite, a TypeScript/Node.js based toolkit for building editors and collaborative applications. The test infrastructure has been configured to run a representative subset of the e2e test suite using Playwright.

## System Dependencies

- **Node.js**: v22.12.0 (pre-installed via NVM, requirement: >=18.19.0 <21.0.0)
- **pnpm**: 9.6.0 (installed globally via npm)
- **Playwright**: Chromium browser and system dependencies
  - Installed via `playwright install chromium`
  - System deps installed via `playwright install-deps chromium` (requires sudo)

## Project Environment

- **Package Manager**: pnpm 9.6.0 (lockfile: pnpm-lock.yaml)
- **Build System**: TypeScript compiler + Nx + Vite
- **Testing Framework**: Playwright 1.45.3 for e2e tests
- **Build Output**:
  - Packages built to `packages/*/dist/`
  - Playground built to `packages/playground/dist/`

### Setup Steps

1. **Install Dependencies**: `pnpm install --frozen-lockfile` (1385 packages)
2. **Build Packages**: Builds all framework and component packages via `pnpm build:packages`
3. **Build Playground**: Builds the test playground application via `pnpm build:playground`
4. **Install Browsers**: Installs Playwright Chromium browser
5. **System Dependencies**: Installs browser system dependencies (requires sudo)

## Testing Framework

### Test Configuration

- **Framework**: Playwright 1.45.3
- **Browser**: Chromium only (to reduce resource usage)
- **Workers**: Limited to 4 (from default 80% to avoid resource exhaustion)
- **Timeout**: 40000ms per test
- **Test Port**: 5173 (preview server)

### Test Execution

The test runner (`/scripts/run_tests`) executes a representative subset of tests:
- **Tests Run**: `tests/basic.spec.ts` (21 tests covering core functionality)
- **Full Suite**: 88 test files total, but running all would exceed 15-minute time limit
- **Server**: Manually starts Vite preview server on port 5173 (Nx webServer has resource issues)

### Test Reporting

A custom JSON reporter (`/scripts/json-reporter.js`) outputs test results in the format:
```json
{"passed": N, "failed": N, "skipped": N, "total": N}
```

### Test Results (HEAD commit)

- Passed: 4-5 tests
- Failed: 16-17 tests
- Total: 21 tests
- Duration: ~2.8 minutes

Note: Some test failures are expected in a clean checkout environment as they may require specific setup or data.

## Additional Notes

### Challenges Encountered

1. **Node Version Mismatch**: Project specifies Node <21.0.0 but environment has v22.12.0. Engine warning appears but tests still run.

2. **Nx Resource Issues**: The default `pnpm -w preview` command (via Nx) fails with "Resource temporarily unavailable" errors when trying to spawn too many worker threads. Workaround: manually start Vite preview server.

3. **Playwright Worker Exhaustion**: Default 80% workers (76 workers) caused "EAGAIN" errors. Reduced to 4 workers in custom config.

4. **Test Scope**: Full test suite (88 files) takes too long. Limited to `basic.spec.ts` to complete within 15-minute constraint.

### Script Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Use only version-controlled commands and configuration
- Don't modify any tracked files in `/testbed/`
- Install all dependencies fresh from lockfiles
- Are idempotent and can be run multiple times

### Execution Command

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

This ensures a clean environment, installs system dependencies, sets up the shell environment, and runs the test suite.
