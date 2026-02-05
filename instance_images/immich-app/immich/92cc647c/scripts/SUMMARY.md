# Summary

This repository is **Immich**, a high-performance self-hosted photo and video management solution. The testing setup focuses on the **server** component, which is a Node.js/TypeScript application built with the NestJS framework.

## System Dependencies

No system-level services are required for running the unit test suite. The tests are designed to run independently without external dependencies like databases or Redis.

### Pre-installed Tools Used
- **Node.js v22.12.0** (managed by nvm)
- **npm 10.9.0** (Node package manager)
- **Python 3** (for test output parsing)

## Project Environment

### Primary Language
- **TypeScript** with **Node.js**
- Framework: **NestJS** (v10.x)

### Package Manager
- **npm** with `package-lock.json` for deterministic builds

### Dependencies Installation
The project dependencies are installed via:
```bash
npm ci --prefer-offline --no-audit
```

This installs ~1200 packages including:
- Testing framework: Jest (v29.6.4)
- TypeScript tooling: ts-jest, ts-node
- NestJS core and testing utilities
- Various domain-specific libraries (sharp, fluent-ffmpeg, bcrypt, etc.)

### Environment Variables
- `TZ=UTC` - Ensures consistent timezone for tests
- `NODE_ENV=test` - Sets environment to test mode

## Testing Framework

### Framework: Jest
- **Test Files**: 32 test suites containing 1,092 unit tests
- **Test Pattern**: `*.spec.ts` files in the `src/` directory
- **Test Type**: Unit tests with mocked dependencies

### Test Execution
Tests are run with:
```bash
npm test -- --json --testLocationInResults --verbose=false --maxWorkers=2
```

### Test Configuration
- Configuration is in `server/package.json` under the `jest` key
- Global setup script: `test/global-setup.js` (sets TZ=UTC)
- Test environment: Node.js (not JSDOM)
- Coverage thresholds are defined for the domain layer

### Test Results
- **Output Format**: JSON (Jest's native JSON output)
- **Parsed Format**: `{"passed": int, "failed": int, "skipped": int, "total": int}`
- **Execution Time**: ~11-12 seconds for full suite

### Mock Strategy
Tests use repository mocks (located in `test/repositories/`) and test fixtures (in `test/fixtures/`) to isolate units under test. No real database or external services are required.

## Additional Notes

### Test Containers
The project includes `@testcontainers/postgresql` as a dev dependency, but this is only used for e2e tests (in `e2e/jobs/`), not for the unit test suite we're running. The unit tests use pure mocking and don't require Docker.

### Warnings During Tests
During test execution, you may see non-critical warnings about:
- Database extensions (pgvecto.rs, pgvector) - these are logged by test code but don't affect test outcomes
- Deprecated npm packages - these don't impact test execution

### Portability
All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification, ensuring backward compatibility across commits.

### Script Organization
- `/scripts/setup_system.sh` - System-level setup (currently no-op as no services needed)
- `/scripts/setup_shell.sh` - Shell environment and dependency setup
- `/scripts/run_tests` - Test execution with JSON output parsing

### Performance
The test suite runs efficiently with 2 parallel workers, completing in approximately 11-12 seconds on the provided environment.
