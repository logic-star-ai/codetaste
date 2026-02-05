# Summary

This document describes the testing setup for Apache DataFusion, a Rust-based query engine.

## System Dependencies

- **Protobuf Compiler (protoc)**: Version 21.4, required for compiling protocol buffer definitions
  - Installed automatically by `setup_shell.sh` to `$HOME/.protoc/`
- **Rust Toolchain**: Version 1.70+ (present in environment: 1.92.0)
- **Git**: For submodule management (parquet-testing and arrow-testing)

No system services (databases, Redis, etc.) are required for running tests.

## Project Environment

- **Language**: Rust
- **Build System**: Cargo (Rust package manager)
- **Workspace Structure**: Multi-crate workspace with 12+ member crates
- **Primary Crates**:
  - `datafusion-common`: Common utilities and error handling
  - `datafusion-core`: Main query engine
  - `datafusion-expr`: Expression system
  - `datafusion-sql`: SQL parsing and planning
  - `datafusion-optimizer`: Query optimization
  - `datafusion-physical-*`: Physical execution layer

### Dependency Management

The project uses specific versions of Apache Arrow (v47.0.0) and related crates. A **critical compatibility issue** exists between `arrow-arith 47.0.0` and `chrono-tz 0.8.x`:
- The `chrono-tz` 0.8 series added a `quarter()` method that conflicts with Arrow's internal implementation
- **Workaround**: The `setup_shell.sh` script automatically patches the `arrow-arith` source in the cargo registry cache to disambiguate the method calls

### Environment Variables

- `CARGO_HOME=/testbed/.cargo-local`: Uses a local cargo directory to persist patched dependencies
- `PATH`: Extended to include protobuf compiler location

## Testing Framework

- **Test Runner**: Cargo's built-in test framework (`cargo test`)
- **Test Command**: `cargo test --lib --tests --bins --features avro,json,backtrace`
  - `--lib`: Tests library code
  - `--tests`: Runs integration tests
  - `--bins`: Tests binary targets
  - `--features avro,json,backtrace`: Enables additional features for comprehensive testing

### Test Output Format

The `run_tests` script:
1. Executes the full test suite
2. Captures stdout/stderr output
3. Parses the test summary line using Python
4. Outputs a single JSON line: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Obstacles and Workarounds

1. **Arrow-Arith Compilation Issue**:
   - **Problem**: `arrow-arith 47.0.0` has a method name collision with `chrono-tz 0.8.x`
   - **Solution**: Automatically patch the extracted arrow-arith source during setup to use fully-qualified method names
   - **Implementation**: `setup_shell.sh` triggers compilation to extract sources, then applies a sed/perl patch to `temporal.rs`

2. **Minimal Environment**:
   - Standard Unix tools (awk, sed, grep with -P) are not available
   - **Solution**: Use Python for parsing test output, which is available in the environment

3. **Git Submodules**:
   - Required for test data (parquet-testing, arrow-testing)
   - Automatically initialized by setup scripts

4. **Cargo Registry**:
   - Uses a local CARGO_HOME (`/testbed/.cargo-local`) instead of the default `~/.cargo`
   - This ensures patched dependencies persist and aren't cleaned between script runs
   - Files in `/testbed/.cargo-local` are gitignored and won't affect `git status`

### Portability

All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications, as the dependency patching is performed dynamically during setup.

### Performance Notes

- Full test suite may take 10-15 minutes to complete
- Compilation is cached in `/testbed/target/` and `/testbed/.cargo-local/`
- First run after `git clean -xdff` requires full dependency download and compilation
