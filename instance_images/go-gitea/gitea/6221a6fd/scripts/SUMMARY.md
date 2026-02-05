# Summary

This repository is **Gitea**, a self-hosted Git service written in Go with a Vue.js frontend. The test setup runs unit tests for both backend (Go) and frontend (JavaScript) code.

## System Dependencies

The following system packages must be installed:
- **git-lfs** (Git Large File Storage) - Required by the test suite for handling large file assets in test repositories

All other dependencies are managed through:
- Go modules (`go.mod`/`go.sum`)
- npm/Node.js (`package.json`/`package-lock.json`)

## Project Environment

### Language and Runtime
- **Primary Language**: Go 1.19+ (tested with Go 1.23.4)
- **Frontend**: Node.js >= 14.0.0 (tested with Node.js 22.12.0)
- **Build Tools**: webpack, npm

### Environment Variables
- `CGO_EXTRA_CFLAGS="-DSQLITE_MAX_VARIABLE_NUMBER=32766"` - Required for SQLite support
- `TEST_TAGS="sqlite sqlite_unlock_notify"` - Test build tags

### Dependencies Installation
1. Go dependencies are automatically downloaded via `go mod download`
2. Node.js dependencies installed via `npm install`
3. Frontend assets built via webpack (`make webpack`)

## Testing Framework

### Backend Tests (Go)
- **Framework**: Go's built-in `testing` package
- **Test Types**: Unit tests (integration and e2e tests excluded from quick suite)
- **Command**: `go test -json -short -tags='sqlite sqlite_unlock_notify'`
- **Scope**: Excludes:
  - `code.gitea.io/gitea/models/migrations`
  - `code.gitea.io/gitea/tests/integration`
  - `code.gitea.io/gitea/tests/e2e`
  - `code.gitea.io/gitea/tests` (package itself)
- **Output Format**: JSON test results parsed for pass/fail/skip counts

### Frontend Tests (JavaScript)
- **Framework**: Vitest (test runner) with jsdom (browser environment)
- **Command**: `npx vitest run`
- **Test Files**: Located in `web_src/**/*.test.js`
- **Configuration**: `vitest.config.js`

### Test Results
On both HEAD and HEAD~1 commits:
- **Passed**: 2325 tests (2305 Go + 20 JS)
- **Failed**: 25 tests (all Go)
- **Skipped**: 10 tests (all Go)
- **Total**: 2360 tests
- **Execution Time**: ~10 minutes total

## Additional Notes

### Script Design
- `setup_system.sh`: Minimal script that exits successfully. No system services are required for SQLite-based tests.
- `setup_shell.sh`: Idempotent setup that installs dependencies and builds frontend assets. Safe to run multiple times.
- `run_tests`: Executes both Go and JavaScript tests, parsing their output to produce a single JSON summary line.

### Portability
All scripts work on both HEAD and HEAD~1 commits without modification, as required. The scripts only modify files that are git-ignored (build artifacts, node_modules, etc.) and never touch version-controlled files.

### Test Coverage
The test suite focuses on **unit tests** to keep execution time under 15 minutes. Integration tests and e2e tests are excluded as they would require:
- Database services (MySQL, PostgreSQL, MSSQL)
- Significantly longer execution time
- Additional system configuration

The unit test suite provides representative coverage of the codebase with 2360 tests across models, modules, routers, and services packages.
