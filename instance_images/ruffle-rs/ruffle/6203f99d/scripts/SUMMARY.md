# Summary

This repository contains Ruffle, an Adobe Flash Player emulator written in Rust. The test suite comprises 2,730 tests that validate SWF file playback, ActionScript Virtual Machine (AVM1 and AVM2) functionality, visual rendering, and various Flash Player features.

## System Dependencies

The following system packages are required for building and testing Ruffle:

- **libasound2-dev**: ALSA sound library development files
- **libxcb-shape0-dev**: X11 XCB shape extension library
- **libxcb-xfixes0-dev**: X11 XCB fixes extension library
- **libgtk-3-dev**: GTK+ 3.0 graphical user interface library
- **libpango1.0-dev**: Pango text rendering library
- **libudev-dev**: libudev development files
- **mesa-vulkan-drivers**: Mesa Vulkan graphics drivers

These dependencies are installed via `apt-get` on the Ubuntu 24.04 system.

## Project Environment

- **Language**: Rust (stable channel, currently 1.92.0)
- **Build System**: Cargo (Rust's package manager)
- **Workspace**: Multi-crate workspace with 35 members including:
  - `core`: Main Ruffle emulator core
  - `desktop`: Desktop application frontend
  - `web`: WebAssembly build for web browsers
  - `tests`: Test framework and regression tests
  - Various rendering backends (wgpu, canvas, webgl)
  - Supporting libraries (swf, flv, wstr, etc.)

### Environment Variables

- `XDG_RUNTIME_DIR`: Set to avoid warnings (dummy value)
- `CARGO_INCREMENTAL=1`: Enables incremental compilation
- `CARGO_NET_GIT_FETCH_WITH_CLI=true`: Uses git CLI for network operations

### Features Used in Tests

- `lzma`: LZMA compression support
- `jpegxr`: JPEG XR image format support

Note: The `imgtests` feature is disabled as it requires visual comparison against CI-generated reference images.

## Testing Framework

The test suite uses a custom test harness based on **libtest-mimic**, which provides flexibility in test discovery and execution.

### Test Structure

- **Test Binary**: `tests/regression_tests.rs` (custom harness with `harness = false`)
- **Test Discovery**: Tests are discovered by scanning for `test.toml` files in the `tests/tests/swfs/` directory hierarchy
- **Test Categories**:
  - `avm1/`: ActionScript 1.0 Virtual Machine tests (~494 tests)
  - `avm2/`: ActionScript 3.0 Virtual Machine tests
  - `visual/`: Visual rendering tests (shapes, filters, blending, text, etc.)
  - `timeline/`: Timeline and scene management tests
  - `fonts/`: Font rendering tests
  - `from_avmplus/`: Tests from Adobe's AVM+ test suite
  - `from_shumway/`: Tests from Mozilla's Shumway Flash player
  - Plus specialized unit tests for shared objects and external interfaces

### Test Execution

- **Command**: `cargo test --package tests --test tests --features lzma,jpegxr`
- **Execution Time**: ~34 seconds for all 2,730 tests
- **Test Results**:
  - 2,539 tests passed
  - 0 tests failed
  - 191 tests ignored (skipped)
  - Total: 2,730 tests

### Test Output Format

The test runner outputs results in the standard cargo test format, which is parsed to extract:
- Passed test count
- Failed test count
- Ignored/skipped test count
- Total test count

The final output is formatted as JSON: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Build Caching

The setup script intelligently checks if the test binary needs rebuilding by:
1. Checking if the test binary exists
2. Comparing modification times of Rust source files against the test binary
3. Only rebuilding if source files are newer or binary doesn't exist

This makes subsequent test runs very fast (~0.2s compile time when cached).

### Portability

The scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification, ensuring they are resilient to minor code changes.

### Test Determinism

Tests are deterministic and produce consistent results across runs. Some tests validate timeouts and error conditions (e.g., script execution timeout), which are properly handled by the test framework.

### No System Services Required

Unlike many projects, Ruffle tests do not require any system services (databases, message queues, etc.) to be running. The `setup_system.sh` script is essentially a no-op.
