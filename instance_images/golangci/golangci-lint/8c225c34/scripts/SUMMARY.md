# Summary

This repository contains golangci-lint, a fast Go linters runner written in Go. The test suite validates the functionality of various linters and the core linting engine.

## System Dependencies

- **Go**: Version 1.23.0+ (currently using Go 1.23.4)
- **System libraries**: Standard Linux build tools (gcc, etc.) for CGO support
- **No additional services**: No database, Redis, or other services are required

## PROJECT Environment

### Language and Runtime
- **Primary Language**: Go
- **Minimum Go Version**: 1.23.0 (as specified in go.mod)
- **Package Manager**: Go modules (go mod)

### Environment Variables
The following environment variables are set for testing:
- `GOLANGCI_LINT_INSTALLED=true`: Indicates golangci-lint is installed
- `GL_TEST_RUN=1`: Marks test execution context
- `CGO_ENABLED=1`: Enables CGO for tests that require it
- `GOPROXY=https://proxy.golang.org`: Uses Go proxy for module downloads

### Build Process
The test setup involves:
1. Downloading Go module dependencies
2. Building the golangci-lint binary from source
3. Running the binary against the codebase itself (self-linting)
4. Executing the full test suite

## Testing Framework

### Test Framework
- **Framework**: Go's built-in testing framework
- **Test Command**: `go test`
- **Test Format**: JSON output for parsing results
- **Parallelism**: Sequential package testing (`-p=1`) and single-threaded test execution (`-parallel 1`) to avoid resource exhaustion
- **Timeout**: 15-minute timeout per test run

### Test Structure
- Tests are located in various `*_test.go` files throughout the codebase
- Integration tests in `/testbed/test/` directory
- Unit tests distributed across `/testbed/pkg/` and `/testbed/internal/` directories
- Tests validate linter behavior, configuration handling, and output formatting

### Test Execution
The test runner performs three main steps:
1. **Self-linting**: Runs golangci-lint on its own codebase
2. **Full test suite**: Executes all Go tests with JSON output
3. **Result parsing**: Parses JSON output to count passed, failed, and skipped tests

### Test Metrics (HEAD commit)
- **Total Tests**: 1,452
- **Passed**: 1,439
- **Failed**: 0
- **Skipped**: 13

## Additional Notes

### Resource Management
The test suite initially encountered "fork/exec: resource temporarily unavailable" errors when running with higher parallelism (`-parallel 2`). This was resolved by:
- Setting `-p=1` to run one package at a time
- Setting `-parallel 1` to run tests sequentially within each package

This conservative approach ensures tests complete successfully without resource exhaustion, though it increases total test execution time.

### Portability
All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. The scripts handle:
- Clean builds from scratch
- Module dependency resolution
- Binary compilation
- Test execution and result reporting

### Test Determinism
Tests are deterministic when run with the specified resource constraints. The JSON output format provides accurate counts of test outcomes, making it easy to track regressions or improvements across commits.
