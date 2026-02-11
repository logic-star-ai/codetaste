# Summary

This repository contains **fq**, a tool for working with binary data formats, written in Go. The project is a jq-like tool that allows you to query, inspect, and debug media codecs, containers, and various binary formats.

## System Dependencies

- **expect**: Required for CLI interactive testing (REPL tests). Installed via `apt-get` in `setup_system.sh`.

## PROJECT Environment

- **Language**: Go (requires 1.20+, tested with 1.23.4)
- **Build Tool**: Go modules (go.mod)
- **Dependencies**: Managed via `go.mod`, automatically downloaded during `go build`
- **Binary Output**: CGO_ENABLED=0 go build produces a static binary named `fq`

### Environment Setup

The environment is configured through:
1. **setup_system.sh**: Installs expect for CLI testing
2. **setup_shell.sh**:
   - Downloads Go dependencies via `go mod download`
   - Builds the `fq` binary in `/testbed`
   - Exports PATH to include `/testbed` for accessing the binary

## Testing Framework

The project uses three types of tests:

1. **Go Unit Tests** (~6661 tests)
   - Standard Go testing framework (`go test`)
   - Test files: `*_test.go` throughout the codebase
   - Run with timeout of 20 minutes
   - Output parsed from JSON format (`go test -json`)

2. **jq Tests** (~3 tests)
   - Custom jq-based test files (`*.jq.test`)
   - Located in `pkg/interp/`
   - Run via the built `fq` binary with the jqtest module
   - Tests the query language functionality

3. **CLI Tests** (~3 tests)
   - Interactive CLI tests using expect scripts (`*.exp`)
   - Tests REPL functionality and control sequences (Ctrl-C, Ctrl-D)
   - Located in `pkg/cli/`
   - Requires expect to be installed

### Test Execution

The `run_tests` script:
- Runs all three test types sequentially
- Parses output from each test type
- Outputs a final JSON summary: `{"passed": N, "failed": N, "skipped": N, "total": N}`
- Typical results: ~6667 passed, 0 failed, 1 skipped

## Additional Notes

- The project requires no virtual environments or special runtime setup
- All dependencies are self-contained in Go modules
- The build is deterministic and produces a static binary
- Tests complete in approximately 2-5 minutes depending on system performance
- The scripts are designed to work on both the current commit and HEAD~1, ensuring portability
- Git status remains clean after running tests (no modifications to versioned files)
