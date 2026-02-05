# Summary

This repository is the **MongoDB Go Driver**, a supported driver for MongoDB in Go. The testing setup executes unit tests using Go's native testing framework with the `-short` flag to skip integration tests that require MongoDB servers.

## System Dependencies

- **Go**: Version 1.23.4 (pre-installed)
- **Python3**: Required for JSON parsing in the test runner script
- **jq**: Available but not used (Python preferred for JSON parsing)
- **No system services required**: Unit tests with `-short` flag don't require MongoDB or other external services

## PROJECT Environment

- **Language**: Go (requires Go 1.13+, Go 1.20+ recommended for running tests)
- **Module**: `go.mongodb.org/mongo-driver`
- **Build System**: Standard Go toolchain with Makefile for additional commands
- **Dependencies**: Managed via `go.mod` and automatically downloaded by `go mod download`
- **Key Environment Variables**:
  - `CGO_ENABLED=1`: Required for certain build features
  - `GOFLAGS=""`: Cleared to avoid conflicts

## Testing Framework

- **Framework**: Go's built-in testing framework (`go test`)
- **Test Execution**: `go test -short -timeout 60s -json ./...`
  - `-short`: Skips integration tests requiring MongoDB server
  - `-timeout 60s`: 60-second timeout per package
  - `-json`: Outputs test results in JSON format for parsing
- **Test Coverage**:
  - Tests across multiple packages: `bson`, `mongo`, `internal/*`, etc.
  - Unit tests for BSON encoding/decoding, data types, utilities
  - 7,143 tests passing, 70 skipped (packages without tests), 0 failures
- **Output Format**: JSON with fields `{passed, failed, skipped, total}`

## Additional Notes

### Test Execution Time
The full test suite completes in approximately 2-3 minutes with the `-short` flag. Without `-short`, tests would require a running MongoDB instance and take significantly longer.

### Script Portability
All scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) work on both HEAD and HEAD~1 commits without modification, as required.

### Integration Tests
The `-short` flag is critical for this setup. Without it, tests would attempt to connect to MongoDB and fail. The Makefile includes various targets for running integration tests (e.g., `evg-test`, `evg-test-atlas`) that require specific MongoDB deployments and environment variables.

### Test Output Parsing
The test runner uses Python to parse JSON output from `go test -json`. Each test result is counted individually (only lines with both `"Action"` and `"Test"` fields), excluding package-level summary lines.
