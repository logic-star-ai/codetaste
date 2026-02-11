# Summary

This repository contains **Bevy**, a data-driven game engine built in Rust. The test infrastructure validates the core engine functionality across 44+ crates in the workspace.

## System Dependencies

The following system packages are required for building and testing Bevy on Linux:

- **libasound2-dev**: ALSA sound library development files (for audio support)
- **libudev-dev**: libudev development files (for device management)

These dependencies are installed via `apt-get` in the `setup_system.sh` script.

## PROJECT Environment

### Runtime Requirements
- **Rust**: Version 1.85.0 or later (project specifies rust-version in Cargo.toml)
- **Current Rust version**: 1.92.0 (pre-installed in the environment)
- **Package Manager**: Cargo (Rust's built-in package manager)

### Environment Variables
The following environment variables are set in `setup_shell.sh` to optimize the test environment:

- `CARGO_TERM_COLOR=always`: Enable colored output
- `CARGO_INCREMENTAL=0`: Disable incremental compilation for consistent builds
- `CARGO_PROFILE_TEST_DEBUG=0`: Reduce debug info in test builds
- `CARGO_PROFILE_DEV_DEBUG=0`: Reduce debug info in dev builds

### Build Process
The setup script builds all workspace crates with their library and test targets using:
```bash
cargo build --workspace --lib --tests
```

## Testing Framework

### Test Command
The test suite uses Rust's built-in test framework via Cargo:
```bash
cargo test --workspace --lib --tests
```

This runs:
- **Library tests** (`--lib`): Unit tests within each crate's library code
- **Integration tests** (`--tests`): Tests in the `tests/` directories

### Test Scope
- **Total Crates**: 44+ workspace members
- **Test Coverage**: Core engine functionality including:
  - ECS (Entity Component System) - bevy_ecs
  - Math primitives and operations - bevy_math
  - Utilities - bevy_utils
  - And many other engine subsystems

### Test Results
On the current HEAD commit (7b1c9f1), the test suite reports:
- **Passed**: 867 tests
- **Failed**: 9 tests
- **Skipped**: 1 test
- **Total**: 877 tests

### Output Format
The `run_tests` script parses cargo test output and produces JSON results in the format:
```json
{"passed": 867, "failed": 9, "skipped": 1, "total": 877}
```

## Additional Notes

### Known Test Failures
There are 9 test failures in the bevy_ecs crate related to error message format validation. These tests expect error messages without lifetime annotations (e.g., `EntityMut`) but Rust 1.92.0 includes lifetime annotations in the output (e.g., `EntityMut<'_>`). The failures are:

1. `query::state::tests::cannot_transmute_entity_ref`
2. `system::system::tests::run_system_once_invalid_params`
3. `system::system_param::tests::missing_event_error`
4. `system::system_param::tests::missing_resource_error`
5. `system::system_registry::tests::run_system_invalid_params`
6. `system::tests::assert_deferred_world_and_entity_ref_system_does_conflict_first`
7. `system::tests::assert_entity_mut_system_does_conflict`
8. `system::tests::assert_entity_ref_and_entity_mut_system_does_conflict`
9. `system::tests::assert_world_and_entity_mut_system_does_conflict_first`

These failures are consistent across both HEAD and HEAD~1 commits, indicating they are likely due to the Rust compiler version (1.92.0) being newer than what the tests were written for (the project specifies minimum Rust 1.85.0).

### Build Time
- Initial dependency download and build: ~90 seconds
- Subsequent builds (cached): <5 seconds
- Test execution: ~15 minutes for full suite

### Portability
The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They handle:
- Clean environment setup from scratch
- Idempotent builds (safe to run multiple times)
- Consistent test output parsing
