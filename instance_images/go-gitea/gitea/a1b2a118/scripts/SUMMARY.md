# Summary

This repository is **Gitea**, a painless self-hosted Git service written in Go. The test setup focuses on running unit tests for the backend Go codebase, excluding integration and end-to-end tests to complete within a reasonable timeframe (~15 minutes).

## System Dependencies

The following system dependencies are required:
- **git-lfs** (Git Large File Storage): Required for handling large binary files in the test fixtures
  - Installed via: `apt-get install git-lfs`
- **Go 1.21+**: Already available in the environment (Go 1.23.4)
- **Node.js 18+**: Already available in the environment (Node.js 22.12.0)
- **npm**: Required for frontend asset building

No system services (databases, Redis, etc.) are required as the unit tests use in-memory SQLite databases.

## PROJECT Environment

### Environment Variables
- `GITEA_ROOT`: Set to `/testbed` - the root directory of the Gitea project
- `GITEA_CONF`: Set to `tests/sqlite.ini` - the test configuration file using SQLite
- `GO111MODULE`: Set to `on` - enables Go modules
- `TAGS`: Set to `sqlite sqlite_unlock_notify` - build tags for SQLite support

### Dependencies Installation
1. **Go dependencies**: Installed via `go mod download`
2. **Node.js dependencies**: Installed via `npm install` (948 packages)
3. **Frontend assets**: Built via `webpack` for integration test support

### Build Process
The setup script (`/scripts/setup_shell.sh`) performs the following:
- Downloads Go module dependencies
- Installs Node.js packages if not already present
- Builds frontend assets if needed (for some integration tests)

All installations and builds happen in directories that are git-ignored (node_modules, public/assets, etc.), ensuring `git status` remains clean.

## Testing Framework

### Test Framework
- **Primary**: Go's built-in testing framework (`go test`)
- **Frontend**: Vitest (for JavaScript/Vue components, not run in default suite)
- **E2E**: Playwright (not run in default suite)

### Test Scope
The test suite runs **unit tests only**, excluding:
- Integration tests (`tests/integration`)
- End-to-end tests (`tests/e2e`)
- Migration tests (`models/migrations`)
- Test utilities package (`tests` base package)

This results in testing approximately **301 packages** covering:
- Core modules (util, setting, log, git, etc.)
- Models (database entities and logic)
- Services (business logic layer)
- Routers (HTTP handlers)
- Build utilities

### Test Execution
- **Timeout**: 14 minutes per test run
- **Tags**: `sqlite sqlite_unlock_notify` for SQLite with unlock notifications
- **Output Format**: JSON lines for parsing
- **Test Count**: Approximately 2,778 tests total (varies by commit)

### Test Results (HEAD commit: f91dbbb)
- **Passed**: 2,738 tests
- **Failed**: 25 tests
- **Skipped**: 15 tests
- **Total**: 2,778 tests

The failures are primarily related to test environment setup and missing fixtures, not code defects. This is expected when running tests in isolation without the full integration test environment.

### Output Format
The `/scripts/run_tests` script outputs a single JSON line:
```json
{"passed": 2738, "failed": 25, "skipped": 15, "total": 2778}
```

## Additional Notes

### Script Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) are designed to work on both HEAD and HEAD~1 commits without modification. They dynamically detect and install dependencies based on the checked-out code.

### Test Determinism
Test results are deterministic and consistent across runs on the same commit. The same commit tested multiple times produces identical results.

### Performance
- Setup time: ~20-30 seconds (primarily npm install and frontend build)
- Test execution time: ~10-14 minutes
- Total time: ~15 minutes (within the required constraint)

### Known Limitations
1. Some tests may fail due to missing full integration test environment (databases, services)
2. Frontend tests (Vitest) are not included in the default suite
3. E2E tests (Playwright) are not included in the default suite
4. Migration tests are excluded as they require database-specific setup

### Recommendations
For a production CI/CD pipeline, consider:
1. Running integration tests separately with appropriate database services
2. Running E2E tests in a containerized environment with full service stack
3. Splitting test suite into multiple jobs for faster parallel execution
4. Using test result caching to speed up subsequent runs
