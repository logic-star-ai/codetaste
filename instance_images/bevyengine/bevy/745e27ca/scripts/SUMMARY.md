# Summary

This testing setup provides environment configuration and test execution scripts for the Bevy game engine repository. The scripts support running a representative subset of core Bevy crates for validation purposes.

## System Dependencies

The following Linux system packages are required and installed via apt:
- **libasound2-dev**: ALSA sound library development files
- **libudev-dev**: udev device management library development files
- **libwayland-dev**: Wayland compositor protocol development files
- **libxkbcommon-dev**: XKB common library development files

These dependencies are installed automatically during the shell setup phase if not already present.

## Project Environment

**Primary Language**: Rust
- **MSRV**: 1.82.0 (project specifies this in Cargo.toml)
- **Current Rust Version**: 1.92.0 (pre-installed in environment)
- **Build Tool**: Cargo (Rust's package manager)

**Environment Variables**:
- `CARGO_TERM_COLOR=always`: Enables colored output
- `CARGO_INCREMENTAL=0`: Disables incremental compilation for faster clean builds
- `RUSTFLAGS="-C debuginfo=0"`: Reduces debug info to speed up compilation

**Testing Scope**: The test suite runs a representative subset of core crates rather than the full workspace to keep execution time under 15 minutes:
- bevy_math
- bevy_utils
- bevy_reflect
- bevy_ecs
- bevy_transform
- bevy_hierarchy
- bevy_time
- bevy_tasks
- bevy_log
- bevy_ptr

This subset covers the most critical foundational crates of the Bevy engine.

## Testing Framework

**Test Runner**: Cargo's built-in test framework

**Test Execution**:
- Command: `cargo test -p <crate> --lib --bins --tests --benches --no-fail-fast`
- The `--no-fail-fast` flag ensures all tests run even when some fail
- Tests are run for libraries, binaries, integration tests, and benchmarks

**Result Parsing**:
The run_tests script parses cargo test output to extract test results. Cargo test outputs summary lines in the format:
```
test result: ok. N passed; M failed; K ignored; ...
```

The script aggregates results from all tested crates and outputs a JSON summary:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Known Issues
- **bevy_mikktspace**: This crate is excluded from the test suite due to compilation errors on the current HEAD commit related to `dangerous_implicit_autorefs` linting. The errors appear to be related to recent changes in Rust's linting that flag unsafe raw pointer dereferencing patterns.

- **Test Failures**: The test suite shows 5 failing tests and 1 skipped test out of 1055 total tests. These appear to be pre-existing failures in bevy_ecs and bevy_reflect crates, not introduced by the testing infrastructure.

### Portability
The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Do not modify versioned files in `/testbed/`
- Only affect build artifacts and dependencies (which are git-ignored)
- Can be run repeatedly with `git clean -xdff` to ensure a clean state

### Performance
- Initial build time: ~5-10 minutes (downloads and compiles dependencies)
- Subsequent test runs: ~2-3 minutes (if dependencies are cached)
- The representative subset approach ensures the full pipeline completes well within the 15-minute target
