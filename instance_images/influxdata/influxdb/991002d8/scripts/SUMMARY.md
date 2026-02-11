# Summary

This testing setup configures and runs the InfluxDB v2.x test suite, which is written in Go.

## System Dependencies

The following system packages are required and installed via `setup_system.sh`:
- **clang**: C/C++ compiler required for CGO compilation
- **llvm-dev / llvm-18-dev**: LLVM development libraries and tools
- **libclang-dev**: Clang library headers
- **bzr**: Bazaar version control system (required by some Go dependencies)

These dependencies are installed via `apt-get` and are necessary for building Go packages that use CGO (C bindings).

## PROJECT Environment

The project is built using:
- **Language**: Go 1.13+ (tested with Go 1.23.4)
- **Build System**: Go modules (GO111MODULE=on)
- **Additional Language**: Rust (for libflux parser, though full compilation is not currently working)
- **Package Manager**: Go modules

### Environment Variables

The `setup_shell.sh` script configures:
- `GO111MODULE=on`: Enable Go modules
- `GOFLAGS="-mod=readonly"`: Use readonly mode for dependencies
- `FLUX_PARSER_TYPE=rust`: Specify Rust-based Flux parser
- `GOTRACEBACK=all`: Enable full stack traces for debugging
- `LLVM_CONFIG_PATH=/usr/bin/llvm-config-18`: Path to LLVM configuration tool
- `PATH`: Extended to include `$HOME/go/bin` for Go binaries

### Project Structure

InfluxDB v2.x combines:
- **InfluxDB 2.x core**: Time series database backend
- **Flux**: Query language (with Rust-based parser)
- **Chronograf**: Web UI components
- **Kapacitor**: Background processing capabilities

Total: 147 Go packages with ~1,349 unit tests

## Testing Framework

The project uses Go's built-in testing framework (`go test`).

### Test Execution

Tests are run using:
```bash
go test -json -count=1 $PACKAGES
```

Where:
- `-json`: Outputs test results in JSON format for parsing
- `-count=1`: Disables test caching to ensure fresh runs
- `$PACKAGES`: All packages except `internal/promqltests` (which has a separate go.mod)

### Test Results

The test suite typically produces:
- **Total tests**: ~1,349 test cases
- **Passed**: ~1,325 tests
- **Failed**: ~15 tests
- **Skipped**: ~9 tests

Test execution time: ~15-20 seconds on a typical system

### Test Output Format

The `run_tests` script outputs exactly one JSON line to stdout:
```json
{"passed": 1325, "failed": 15, "skipped": 9, "total": 1349}
```

This format is parsed from Go's JSON test output by counting unique top-level test cases (excluding subtests to avoid double-counting).

## Additional Notes

### Libflux Compilation Issue

The project depends on the Flux query language library which includes Rust components (libflux). However, the current version of libflux (v0.64.0) uses `wasm-bindgen v0.2.55`, which is incompatible with modern Rust compilers (Rust 1.92.0).

**Impact**: The `libflux` tag cannot be used, and tests requiring the Flux Rust parser are not fully tested. However, the vast majority of Go unit tests run successfully without the Rust components.

**Workaround**: The `setup_shell.sh` script attempts to generate the `.cgo_ldflags` file but gracefully handles failure, creating an empty file to avoid repeated attempts. Tests that don't require libflux run normally.

### Test Failures

Some tests fail consistently (approximately 15 out of 1,349). These appear to be:
- Static analysis failures (go vet issues with Printf formatting)
- Type conversion warnings
- Pre-existing test failures unrelated to the environment setup

These failures are deterministic and appear on both HEAD and HEAD~1 commits.

### Performance

- First run: ~15-20 seconds (includes dependency downloads)
- Subsequent runs: ~15 seconds (dependencies cached)
- The test suite is relatively fast and suitable for CI/CD pipelines

### Portability

The scripts are designed to work on both the current commit and previous commits (HEAD~1), making them suitable for regression testing and continuous integration.
