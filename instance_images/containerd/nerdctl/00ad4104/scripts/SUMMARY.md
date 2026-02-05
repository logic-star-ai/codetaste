# Summary

This repository contains **nerdctl**, a Docker-compatible CLI for containerd written in Go. The testing setup focuses on running unit tests for the various Go packages in the project.

## System Dependencies

- **Go 1.23.0+**: Required by go.mod (installed: Go 1.23.4)
- **No system services required**: Unit tests do not require containerd or other system services

## Project Environment

- **Language**: Go
- **Go Version**: 1.23.0 (as specified in go.mod)
- **Build System**: Go modules + Makefile
- **Package Manager**: Go modules (go.mod/go.sum)
- **Test Tool**: `gotestsum` (installed automatically by setup_shell.sh)

### Environment Variables

- `GOPATH`: Set to `${HOME}/go`
- `PATH`: Extended to include Go binaries and `${GOPATH}/bin`

### Setup Process

1. **setup_system.sh**: No-op for unit tests (system services not required)
2. **setup_shell.sh**:
   - Installs `gotestsum` test runner
   - Downloads Go module dependencies
   - Builds the nerdctl binary to verify compilation
3. **run_tests**: Runs unit tests for all packages under `./pkg/...`

## Testing Framework

- **Framework**: Go's built-in testing framework (`go test`)
- **Test Runner**: Standard `go test` with verbose output
- **Test Location**: Unit tests in `./pkg/` subdirectories (166 test files)
- **Test Naming**: Files ending with `_test.go`

### Test Results

On a clean checkout, the test suite runs:
- **101 tests pass**
- **2 tests fail** (expected failures on Linux without systemd-resolved):
  - `pkg/mountutil`: Tests requiring mount capabilities
  - `pkg/resolvconf`: Tests requiring `/run/systemd/resolve/resolv.conf`
- **2 tests skip**
- **105 total tests**

### Test Execution

The tests are executed with:
```bash
go test -v ./pkg/...
```

Results are parsed to count:
- Passed: Lines matching `^--- PASS:`
- Failed: Lines matching `^--- FAIL:`
- Skipped: Lines matching `^--- SKIP:`

## Additional Notes

### Known Issues

1. **Expected Test Failures**: Two test failures are expected in this environment:
   - `pkg/mountutil`: Requires specific mount capabilities not available in container
   - `pkg/resolvconf/TestGet`: Expects systemd-resolved which is not running

These failures are environmental and do not indicate broken functionality.

### Portability

The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Use relative paths from the repository root
- Don't modify versioned files (only build artifacts in `_output/`)
- Are idempotent (safe to run multiple times)

### Test Coverage

The unit tests cover:
- Command builders and parsers
- Docker Compose service configuration
- Network utilities and subnet management
- Container utilities and port management
- Image reference parsing
- Configuration file handling
- Store management
- String utilities and formatters

Integration tests (requiring containerd daemon) are available in `cmd/nerdctl/` but are not executed by these scripts as they require additional system setup.
