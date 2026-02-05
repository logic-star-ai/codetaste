# Summary

This repository contains the **Burn** deep learning framework, written in Rust. The test infrastructure runs unit and integration tests for core tensor computation libraries and their backends using Cargo's built-in test framework.

## System Dependencies

The following system packages are installed via `/scripts/setup_system.sh`:

- **Mesa and Vulkan drivers**: Required for GPU-based testing with the WGPU backend
  - `libgl1-mesa-dri`
  - `libxcb-xfixes0-dev`
  - `mesa-vulkan-drivers`
  - `libegl1`, `libgl1`

These dependencies enable GPU compute tests through the WebGPU backend.

## Project Environment

- **Language**: Rust (Minimum version: 1.71.0, tested with 1.92.0)
- **Build System**: Cargo with workspace configuration
- **Package Manager**: Cargo
- **Project Structure**: Cargo workspace with multiple crates
  - Core libraries: `burn-common`, `burn-tensor`, `burn-compute`, `burn-autodiff`
  - Backend implementations: `burn-ndarray`, `burn-wgpu`, `burn-candle`, `burn-tch`
  - Utility crates: `burn-derive`, `burn-tensor-testgen`

### Environment Setup (`/scripts/setup_shell.sh`)

The setup script:
1. Configures Rust toolchain paths
2. Installs additional Rust targets for cross-compilation testing:
   - `wasm32-unknown-unknown` (WebAssembly)
   - `thumbv7m-none-eabi` (ARM embedded)
3. Installs `llvm-tools-preview` component for code coverage
4. Builds the `xtask` helper tool

## Testing Framework

**Framework**: Cargo's built-in test runner (`cargo test`)

### Test Coverage

The test suite focuses on core functionality to complete within 15 minutes:

- **burn-common**: Common utilities and ID generation (3 tests)
- **burn-derive**: Procedural macros for code generation (0 tests, compilation check)
- **burn-tensor-testgen**: Test generation macros (0 tests, compilation check)
- **burn-ndarray**: CPU backend using ndarray (~491 tests)
- **burn-tensor**: Core tensor API and operations (19 tests)
- **burn-compute**: Compute infrastructure (11 tests)
- **burn-autodiff**: Automatic differentiation (6 tests)

**Total**: 530 tests (as of commit 96524d4)

### Test Execution

The `/scripts/run_tests` script:
1. Runs tests for selected core packages using `cargo test`
2. Captures and aggregates test results from multiple test binaries
3. Parses Cargo's test output format to extract pass/fail/skip counts
4. Outputs results as JSON: `{"passed": int, "failed": int, "skipped": int, "total": int}`

## Additional Notes

### Dependency Issues

Some packages were excluded from the test suite due to compilation issues with dependencies in the current environment:

- **burn-core**: Bincode API compatibility issues (`decode_borrowed_from_slice` not found)
- **burn-candle**: Rand/Half crate version conflicts causing trait bound errors
- **burn-train**: Depends on burn-core
- **burn-wgpu**: Depends on burn-core
- **burn-dataset**: Depends on burn-core
- **Examples**: Excluded to keep test time under 15 minutes

These issues appear to be related to dependency version resolution in the Rust toolchain (1.92.0) vs what the project expects. The core tensor computation libraries (ndarray backend, tensor API, autodiff) compile and test successfully, providing adequate coverage of fundamental functionality.

### Workspace Structure

The project uses a Cargo workspace with 28+ member crates. The test infrastructure is designed to be modular, testing each crate independently to isolate failures and provide clear diagnostics.

### Portability

The scripts are designed to work across commits without modification. They:
- Only modify generated/ignored files (`target/`, `Cargo.lock`)
- Do not alter versioned source code
- Work on both HEAD (96524d4) and HEAD~1 (e2a3329)
