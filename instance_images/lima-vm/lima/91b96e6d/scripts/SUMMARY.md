# Summary

This document describes the testing setup for the Lima project (Linux Machines), a virtual machine launcher for Linux on macOS and other platforms.

## System Dependencies

**No system-level dependencies are required for running the unit test suite.**

The Lima project uses Go as its primary programming language. The unit tests run without requiring any system services, virtual machines, or external tools. All tests are pure Go unit tests that validate the core functionality of the Lima codebase.

### Pre-installed Components
- Go 1.24.0 (as specified in go.mod) - available at `/usr/local/go/bin/go`
- GCC toolchain (for CGO support)
- Standard Linux utilities

## Project Environment

### Language and Runtime
- **Primary Language**: Go
- **Required Version**: Go 1.24.0 (minimum as specified in go.mod)
- **Go Modules**: Enabled (GO111MODULE=on)
- **CGO**: Enabled (CGO_ENABLED=1) - required for the hostagent's DNS resolver

### Build System
- **Build Tool**: GNU Make
- **Build Target**: `make limactl` to build the main binary
- **Output Directory**: `_output/bin/`

### Environment Variables
The following environment variables are configured by `/scripts/setup_shell.sh`:
- `GOTOOLCHAIN=auto` - Allows Go to automatically select the correct toolchain version
- `GO111MODULE=on` - Ensures Go modules are enabled
- `CGO_ENABLED=1` - Required for proper DNS resolution in the hostagent

## Testing Framework

### Test Framework
- **Framework**: Go's built-in testing framework (`testing` package)
- **Test Command**: `go test -json ./...`
- **Test Discovery**: All files matching `*_test.go` pattern

### Test Statistics
The test suite includes:
- **Total Tests**: 421 tests
- **Passing Tests**: 418 tests
- **Skipped Tests**: 3 tests (typically fuzz tests in short mode)
- **Failed Tests**: 0 tests

### Test Coverage
Tests are distributed across multiple packages including:
- Command-line interface tests (`cmd/limactl/editflags`)
- Core package tests (`pkg/*`)
- CI data generation tests (`pkg/cidata`)
- Lima YAML configuration tests (`pkg/limayaml`)
- Store management tests (`pkg/store`)
- And many more...

### Test Execution
Tests execute quickly (typically under 1 minute) as they are unit tests without VM instantiation or integration testing. The tests validate:
- Configuration parsing and validation
- Template rendering
- Network configuration
- File path handling
- YAML schema validation
- And other core functionality

## Additional Notes

### Script Design
The scripts are designed to be:
1. **Idempotent**: Safe to run multiple times without side effects
2. **Portable**: Work on both HEAD and HEAD~1 commits
3. **Non-invasive**: Do not modify versioned files in `/testbed/`
4. **Clean**: Use `git clean -xdff` to ensure clean state before each run

### Build Artifacts
All build artifacts are placed in `_output/` directory which is git-ignored. The build process:
1. Downloads Go module dependencies
2. Builds the main `limactl` binary
3. Copies helper scripts to the output directory

### Testing Approach
The test suite focuses on unit tests rather than integration tests. Integration tests that require:
- QEMU or VZ virtualization
- Actual VM instantiation
- Network services
- Container engines

These are handled separately in the GitHub Actions CI pipeline and are not part of this unit test suite.

### Go Version Management
The project requires Go 1.24.0 as specified in the go.mod file. The setup uses `GOTOOLCHAIN=auto` to allow Go's automatic toolchain management to download and use the correct version if needed.

### Verification
Both the current commit (HEAD) and the previous commit (HEAD~1) have been tested successfully:
- Current commit (22af485): 418 passed, 0 failed, 3 skipped, 421 total
- Previous commit (91b96e6): 418 passed, 0 failed, 3 skipped, 421 total

The test results are deterministic and consistent across commits.
