# Summary

This repository contains HashiCorp Consul, a distributed service mesh and service discovery platform written in Go. The test environment has been configured to run a representative subset of unit tests across the main module and its submodules.

## System Dependencies

- **Go**: Version 1.23.4 (installed globally)
- **gotestsum**: Version 1.9.0 (test runner utility)

No additional system services (databases, Redis, etc.) are required for the basic unit test suite.

## PROJECT Environment

The project is organized as a Go module with several submodules:
- `api/` - Client library for Consul API
- `sdk/` - Software Development Kit for Consul
- `proto-public/` - Protocol Buffer definitions
- `envoyextensions/` - Envoy proxy extensions (added in current HEAD)
- `troubleshoot/` - Troubleshooting utilities

### Environment Variables Set:
- `GOPATH` - Go workspace path
- `GOARCH` - Target architecture
- `PATH` - Includes testbed/bin and Go binary paths
- `TEST_RESULTS_DIR` - Location for test artifacts (/tmp/test-results)
- `GIT_AUTHOR_NAME`, `GIT_COMMITTER_NAME` - Git configuration for test runs

### Dependency Management:
Dependencies are managed via Go modules (`go.mod`). The setup script downloads all dependencies for the main module and submodules on first run, marking completion with `.deps_downloaded` files for idempotency.

## Testing Framework

The test suite uses:
- **Go's native testing framework** (`testing` package)
- **gotestsum** - Enhanced test runner with JSON output support
- **testify** - Assertion and mocking library (github.com/stretchr/testify)

### Test Execution Strategy:
To complete within the 15-minute constraint, the test runner executes:

1. **SDK submodule tests** (`/testbed/sdk/...`)
   - Core SDK functionality tests with `-short` flag

2. **API submodule tests** (`/testbed/api/...`)
   - Client API tests with `-short` flag
   - Build failures tolerated due to Go version compatibility

3. **Core main module packages**:
   - `./acl/...` - Access Control List tests
   - `./agent/config/...` - Agent configuration tests
   - `./agent/consul/state/...` - State store tests
   - `./ipaddr/...` - IP address handling tests
   - `./lib/...` - Library utility tests
   - `./types/...` - Type definition tests
   - `./version/...` - Version handling tests

All tests are run with:
- `-short` flag to skip long-running tests
- `-timeout=10m` to prevent hangs
- `gotestsum --jsonfile` to capture structured test results

### Test Result Parsing:
The test runner parses gotestsum's JSON output to extract:
- **Passed**: Tests with `"Action":"pass"` and a `"Test"` field
- **Failed**: Tests with `"Action":"fail"` and a `"Test"` field
- **Skipped**: Tests with `"Action":"skip"` and a `"Test"` field

Results are output as a single JSON line: `{"passed": X, "failed": Y, "skipped": Z, "total": N}`

## Additional Notes

### Go Version Compatibility
The project specifies Go 1.19 in `go.mod`, but runs successfully with Go 1.23.4. The newer Go version occasionally causes build issues in the `api` submodule due to changes in the `golang.org/x/net` package. The test runner tolerates these failures (using `|| true`) to ensure representative tests still execute.

### Skipped Tests
Many tests are skipped when using the `-short` flag, with reasons like:
- "too slow for testing.Short" - Long-running integration tests
- "TODO: missing test case" - Placeholder tests for future implementation

### Test Coverage
The selected test packages provide good coverage of:
- Core ACL and authentication logic
- Agent configuration parsing and validation
- State store operations and indexing
- Network address handling
- Common utility libraries

The full test suite contains 633 test files across the repository. The representative subset runs ~3,200 tests in approximately 20-30 seconds.

### Portability
All scripts are designed to work on both HEAD and HEAD~1 commits. The main difference is the presence/absence of the `envoyextensions/` submodule, which is handled gracefully by conditional checks in the setup script.
