# Summary

This repository contains **vcluster**, a virtual Kubernetes cluster project written in Go. The testing infrastructure has been set up to run the unit test suite for this project.

## System Dependencies

- **Go**: Version 1.23.4 (compatible with project requirement of 1.22.4)
- **jq**: Used for parsing JSON test output
- **Standard build tools**: Pre-installed in the environment

No additional system-level services (databases, Redis, etc.) are required for running the unit tests.

## Project Environment

The project uses the following configuration:

- **Language**: Go
- **Go Module**: github.com/loft-sh/vcluster
- **Required Go Version**: 1.22.4 (as specified in go.mod)
- **Dependency Management**: Vendored dependencies (uses `vendor/` directory)
- **Build System**: Uses Just and GoReleaser for building, but tests are run directly with `go test`

### Environment Variables

The following environment variables are required for testing:
- `GO111MODULE=on`: Enables Go modules
- `GOFLAGS=-mod=vendor`: Forces Go to use vendored dependencies

## Testing Framework

The project uses **Go's built-in testing framework** with the following characteristics:

- **Test Files**: 57 test files matching the pattern `*_test.go`
- **Test Packages**: Unit tests are located in various packages under `pkg/` and `config/`
- **Test Execution**: Tests are run with race detection enabled (`-race` flag in the original test script)
- **Output Format**: JSON format (`-json` flag) for structured test result parsing
- **Coverage**: Tests include coverage profiling capabilities

### Test Categories

The test suite excludes:
- E2E tests located in the `test/` directory (requires Kubernetes cluster)
- Vendor directory tests

### Test Results

Current test suite results:
- **Passed**: 62 tests
- **Failed**: 0 tests
- **Skipped**: 1 test
- **Total**: 63 tests

The test suite completes in approximately 60-90 seconds on a typical development machine.

## Additional Notes

### Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modifications, making them suitable for CI/CD pipelines and historical testing.

### Test Output

The `/scripts/run_tests` script produces a single JSON line to stdout in the format:
```json
{"passed": int, "failed": int, "skipped": int, "total": int}
```

This makes it easy to parse results programmatically for CI/CD integration.

### Excluded Tests

The E2E test suites (located in `/testbed/test/`) are not included in this test runner as they require:
- A running Kubernetes cluster
- Docker image building
- Network connectivity
- Additional infrastructure setup

These E2E tests would need separate infrastructure provisioning and are beyond the scope of the unit testing setup.
