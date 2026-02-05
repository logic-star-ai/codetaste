# Summary

This repository is **Pulumi**, an infrastructure-as-code platform that uses general-purpose programming languages. The project is primarily written in **Go** with additional SDKs in Node.js, Python, and .NET.

## System Dependencies

The project requires:
- **Go 1.20+** (tested with Go 1.23.4)
- Python 3 (for build scripts)
- No system services are required for unit tests

No additional system packages or running services (like databases or Redis) are needed for the unit test suite.

## Project Environment

The setup configures:

1. **Go environment variables:**
   - `GOPATH`: Set to `${HOME}/go`
   - `GOPROXY`: Set to `https://proxy.golang.org`
   - Go binary paths added to PATH

2. **Pulumi-specific environment:**
   - `PULUMI_ROOT=/tmp/pulumi`: Temporary Pulumi installation directory
   - `PULUMI_BIN=/tmp/pulumi/bin`: Binary installation path
   - `PULUMI_HOME=/tmp/pulumi/home`: Pulumi home directory
   - `PULUMI_DISABLE_AUTOMATIC_PLUGIN_ACQUISITION=true`: Prevents automatic plugin downloads

3. **Test configuration:**
   - `GO_TEST_PARALLELISM=8`: Number of parallel tests within a package
   - `GO_TEST_PKG_PARALLELISM=2`: Number of parallel packages to test
   - `GO_TEST_SHUFFLE=off`: Test execution order (deterministic)
   - `GO_TEST_RACE=false`: Race detector disabled for speed

4. **Module structure:**
   The project has three separate Go modules:
   - `/testbed/pkg`: Core Pulumi implementation
   - `/testbed/sdk`: SDK libraries
   - `/testbed/tests`: Integration tests

   Dependencies are downloaded for all three modules during setup.

## Testing Framework

The project uses **Go's built-in testing framework** with the following structure:

- **Test runner:** Custom Python wrapper script (`/scripts/run_tests`) that:
  - Executes `go test` with JSON output format
  - Runs tests in short mode (`-short` flag) to skip long-running tests
  - Parses JSON output to extract test statistics
  - Outputs results in standardized JSON format

- **Test selection:** The test suite runs a representative subset of fast unit tests from the `pkg` module covering:
  - `backend/...`: Backend implementations
  - `resource/...`: Resource management
  - `resource/stack/...`: Stack operations
  - `util/...`: Utility functions
  - `workspace/...`: Workspace management

- **Test execution:**
  - Tests run with `-count=1` to disable caching
  - 15-minute timeout per test run
  - Race detector disabled for faster execution
  - JSON output for deterministic parsing

- **Expected results:** Approximately 1245-1250 tests pass consistently across commits.

## Additional Notes

### Build Issues
During development, there was a linking error when attempting to build the full Pulumi CLI binary:
```
link: github.com/pgavlin/text/internal/bytealg: invalid reference to internal/bytealg.MaxLen
```

This error does not affect unit test execution, as tests run directly via `go test` without requiring a pre-built binary. Integration tests that depend on the Pulumi CLI binary are excluded from this test suite.

### Idempotency
The `/scripts/setup_shell.sh` script is idempotent:
- Uses a flag file (`/tmp/.pulumi_deps_installed`) to avoid re-downloading dependencies
- Can be safely sourced multiple times
- Checks for existing builds before rebuilding

### Portability
All scripts are designed to work on both the current commit (HEAD) and previous commits (HEAD~1) without modification, as verified during testing.

### Test Coverage
The selected test subset provides good coverage of core functionality while completing in under 5 minutes, making it suitable for rapid validation during development.
