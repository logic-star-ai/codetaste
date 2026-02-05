# Summary

This repository contains the Rancher management server written in Go with Python-based integration tests. The setup scripts have been configured to build the Go binary and run the Python test suite.

## System Dependencies

No additional system-level services are required. The setup uses:
- **Go 1.23.4** (pre-installed) - For building the Rancher server binary
- **Python 3.8** (via uv) - For running the integration test suite
- **Git** - For version control operations

## Project Environment

### Go Build Setup
- **Language**: Go with vendor-based dependency management
- **Module**: github.com/rancher/rancher
- **Build approach**: Creates a minimal `go.mod` file to enable `go build -mod=vendor`
- **Build tags**: Uses `-tags k8s` for Kubernetes integration
- **Binary output**: `/testbed/bin/rancher`

### Python Test Environment
- **Python version**: 3.8.20 (managed via uv)
- **Virtual environment**: `/testbed/.venv`
- **Test dependencies**:
  - pytest 3.0.2 (test framework)
  - pytest-xdist (parallel test execution)
  - pytest-repeat (test repetition)
  - cattle 0.5.3 (Rancher API client)
  - requests, pyyaml, netaddr (utilities)
  - websocket-client, PyJWT (communication)

## Testing Framework

- **Framework**: pytest with xdist for parallel execution
- **Test location**: `/testbed/tests/core/`
- **Test approach**: Integration tests that require a running Rancher server
- **Server startup**: The test script starts the Rancher binary with `--add-local` flag
- **Endpoints**: Tests connect to https://localhost:8443/v3 (HTTPS API) and http://localhost:8080/ping (health check)
- **Test execution**: `python -m pytest -v --tb=short -n auto`

## Additional Notes

### Known Issues

1. **HEAD commit build failure** (c563885): The most recent commit "Rename cluster to user and put all controllers in controllers package" has a vendor/code mismatch. The code references `github.com/rancher/norman/types/convert/schemaconvert` which doesn't exist in the vendored dependencies. This prevents the Go binary from being built on the HEAD commit.

2. **Runtime compatibility**: The Go binary built successfully on HEAD~1 (commit 8f9b69f) but exhibits runtime issues when executed with Go 1.23.4, including:
   - Duplicate proto type registration warnings
   - Base64 encoding alphabet panic from the ugorji/go/codec package
   - These are likely due to Go 1.23 being significantly newer than what this codebase was designed for (appears to target Go 1.8-1.11 era based on the Kubernetes v1.8.6 dependency)

3. **Vendor directory structure**: This project uses old-style Go vendoring (pre-modules) from Go 1.5-1.16 era. Modern Go (1.17+) requires a go.mod file even when using vendor mode, so the setup script creates a minimal go.mod if one doesn't exist.

### Workarounds Implemented

- **go.mod creation**: Setup script automatically creates a minimal go.mod to enable modern Go's vendor mode
- **Error handling**: Build failures are properly detected and reported
- **Dependency resolution**: Python dependency conflicts (gdapi-python version mismatch) are non-fatal warnings

### Testing Recommendations

For successful test execution, it's recommended to:
1. Use an older Go version (1.11-1.16) that better matches the codebase era
2. Run tests on HEAD~1 (8f9b69f) which has consistent vendor dependencies
3. Consider updating vendor dependencies on HEAD to match the code changes

### Portability

The scripts are designed to work on both HEAD and HEAD~1 commits:
- `/scripts/setup_system.sh` - No-op script (no system services needed)
- `/scripts/setup_shell.sh` - Sets up Python venv, dependencies, and builds Go binary
- `/scripts/run_tests` - Starts Rancher server, waits for readiness, runs pytest, outputs JSON results

All build artifacts and dependencies are installed in gitignored locations (.venv, bin/, build/, /tmp/rancher-gopath) to maintain a clean working tree.
