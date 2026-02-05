# Summary

This repository contains the Boa JavaScript engine, a Rust-based implementation of the ECMAScript specification. The testing environment has been successfully configured to run the comprehensive test suite using cargo-nextest.

## System Dependencies

No system-level dependencies or services are required beyond the pre-installed Rust toolchain (version 1.92.0, which exceeds the minimum required version of 1.85.0).

The project uses:
- **Language**: Rust
- **Build Tool**: Cargo
- **Test Framework**: cargo-nextest
- **Required Rust Version**: 1.85.0 (installed: 1.92.0)

## Project Environment

### Build Configuration
- **Profile**: `ci` (optimized for continuous integration)
- **Features**: `annex-b`, `intl_bundled`, `experimental`, `embedded_lz4`
- **Workspace**: Multi-crate workspace with core libraries, CLI, FFI bindings, and examples

### Setup Process
1. **setup_system.sh**: No system services required (exits 0)
2. **setup_shell.sh**:
   - Installs cargo-nextest if not present
   - Builds all targets with ci profile
   - Builds tests with required features
3. **run_tests**: Executes tests and outputs JSON results

### Environment Variables
No special environment variables are required. The setup scripts handle all necessary configuration.

## Testing Framework

The project uses **cargo-nextest**, a modern test runner for Rust that provides:
- Parallel test execution
- Better output formatting
- Faster test runs compared to standard `cargo test`

### Test Configuration
- Test profile defined in `.config/nextest.toml`
- Fail-fast disabled for CI to run complete test suite
- Features enabled: `annex-b`, `intl_bundled`, `experimental`, `embedded_lz4`

### Test Results
Current test metrics (as of commit d642599):
- **Total tests**: 1225
- **Passed**: 1225
- **Failed**: 0
- **Skipped**: 2

Test execution time: ~31-35 seconds

### Test Coverage
The test suite includes:
- Unit tests for core engine components (AST, parser, engine, GC)
- Built-in object tests (Array, Date, Math, String, etc.)
- Internationalization tests
- Runtime tests (console, URL, intervals)
- Macro tests (derive macros for JS interop)
- Parser tests including stress tests

## Additional Notes

### Workspace Structure
The project is organized as a Cargo workspace with the following main components:
- `core/*`: Core libraries (ast, engine, gc, parser, runtime, etc.)
- `cli`: Command-line interface
- `ffi/*`: Foreign function interface bindings (WebAssembly)
- `tests/*`: Test utilities and test262 runner
- `examples`: Example usage code
- `tools/*`: Build and development tools

### Build Warnings
Some expected warnings during compilation:
- Unused methods and associated constants
- Unnecessary parentheses (style warnings)
- Dead code in parser and engine

These warnings are part of the normal build process and do not affect test execution.

### Portability
The setup scripts are designed to work across commits (tested on HEAD and HEAD~1) without modification. They handle:
- Automatic installation of cargo-nextest if missing
- Clean builds from scratch after `git clean -xdff`
- Idempotent execution (safe to run multiple times)

### Dependencies Installation
The first run of `setup_shell.sh` downloads and compiles approximately 600+ Rust crates, which takes several minutes. Subsequent runs are much faster due to Cargo's caching.
