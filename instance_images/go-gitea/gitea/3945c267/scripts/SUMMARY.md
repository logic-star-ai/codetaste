# Summary

This repository contains Gitea, a self-hosted Git service written in Go. The test suite consists of backend unit tests covering the core Go packages. The testing framework uses Go's built-in testing package with support for SQLite database.

## System Dependencies

- **git-lfs**: Required for Git Large File Storage support in tests
  - Installed via apt-get during system setup
  - Version: 3.4.1-1ubuntu0.3 (Ubuntu 24.04)

## Project Environment

- **Language**: Go 1.21+ (tested with Go 1.23.4)
- **Build Tags**: `sqlite sqlite_unlock_notify`
- **Database**: SQLite3 with unlock_notify support
- **Package Manager**: Go modules (go mod)
- **Dependencies**: ~200+ Go packages installed via `go mod download`

### Environment Variables

- `GITEA_ROOT`: Set to `/testbed` (project root)
- `GOPATH`: Set to `${HOME}/go`
- `CGO_CFLAGS`: Set to `-DSQLITE_MAX_VARIABLE_NUMBER=32766` for SQLite support
- `TEST_TAGS`: Set to `sqlite sqlite_unlock_notify`

### Build Process

1. Go dependencies are downloaded via `go mod download`
2. Gitea binary is built with SQLite tags: `go build -tags='sqlite sqlite_unlock_notify'`
3. The binary is required by the test framework for some integration-related unit tests

## Testing Framework

- **Framework**: Go testing (`go test`)
- **Output Format**: JSON for programmatic parsing
- **Test Categories**: Backend unit tests across all Go packages
- **Excluded Packages**:
  - `code.gitea.io/gitea/models/migrations/...` (migration tests)
  - `code.gitea.io/gitea/tests/integration/migration-test` (integration migration tests)
  - `code.gitea.io/gitea/tests` (test utilities)
  - `code.gitea.io/gitea/tests/integration` (integration tests)
  - `code.gitea.io/gitea/tests/e2e` (end-to-end tests)

### Test Execution

Tests are run with:
- Timeout: 15 minutes
- Tags: `sqlite sqlite_unlock_notify`
- JSON output for parsing

### Test Results (HEAD: cf0df02)

- **Total**: 2782 tests
- **Passed**: 2742 tests
- **Failed**: 25 tests (SSH key-related, require ssh-keygen)
- **Skipped**: 15 tests

## Additional Notes

### Known Issues

1. **SSH Key Tests**: 25 tests fail due to missing `ssh-keygen` utility
   - Affected packages: `code.gitea.io/gitea/models/asymkey`, `code.gitea.io/gitea/services/asymkey`, `code.gitea.io/gitea/routers/web/repo/setting`
   - These tests verify SSH key parsing and fingerprint calculation
   - Not critical for core functionality testing

### Portability

The test setup scripts are designed to work on both HEAD and HEAD~1:
- Scripts use relative paths and environment variables
- No hard-coded commit references
- Idempotent setup operations (safe to run multiple times)

### Performance

- Initial setup (clean): ~2-3 minutes (includes Go dependency download and binary build)
- Subsequent runs: ~30 seconds (cached dependencies)
- Test execution: ~10-12 minutes for full suite
