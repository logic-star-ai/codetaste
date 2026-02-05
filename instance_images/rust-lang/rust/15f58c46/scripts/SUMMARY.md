# Summary

This setup configures the Rust compiler repository for running representative library tests. The approach uses the stage0 (beta) compiler downloaded by the bootstrap system to avoid the lengthy process of building a full stage1 compiler, which would require building LLVM and the entire Rust toolchain.

## System Dependencies

The following system dependencies are pre-installed and required:
- Python 3.6+ (for x.py bootstrap script)
- Git (for repository management)
- GCC/G++ (C/C++ compiler toolchain)
- Clang (alternative C/C++ compiler)
- CMake (build system generator)
- Ninja (fast build system, though disabled in config to avoid LLVM build)
- pkg-config (dependency discovery tool)
- libssl-dev (OpenSSL development libraries for Cargo)
- Standard build tools (make, binutils, etc.)

No additional system dependencies need to be installed - all are available in the pre-configured Ubuntu 24.04 environment.

## Project Environment

### Language and Build System
- **Language**: Rust
- **Build System**: x.py (custom Python-based bootstrap build system)
- **Package Manager**: Cargo (bundled with Rust toolchain)

### Configuration
The setup creates a `bootstrap.toml` configuration file with the following key settings:

```toml
[llvm]
download-ci-llvm = false  # Avoid downloading unavailable CI LLVM builds
ninja = false             # Disable ninja to skip LLVM compilation

[build]
extended = false          # Build only core components
jobs = 0                  # Use all available CPUs
build-stage = 0          # Use stage0 compiler
test-stage = 0           # Run tests at stage0

[rust]
debug-assertions = false  # Disable to use stage0 compiler without rebuilding
incremental = true        # Enable incremental compilation
```

### Build Process
- **Stage0**: The bootstrap system downloads a pre-built beta compiler from Rust's distribution servers
- **No LLVM Build**: By using stage0 and disabling LLVM downloads, we avoid the time-consuming LLVM compilation
- **No Stage1 Build**: Tests run directly with the stage0 compiler, avoiding the need to build a stage1 compiler

This approach dramatically reduces build time from potentially hours to minutes.

## Testing Framework

### Test Suite
The test runner executes the **library/core** test suite, which includes:
- Core library unit tests (coretests)
- Core library documentation tests (doctes)
- Comprehensive coverage of fundamental Rust data structures and primitives

### Test Execution
- **Command**: `./x.py test --stage 0 --no-fail-fast library/core`
- **Stage**: Stage 0 (using downloaded beta compiler)
- **Test Count**: ~7,600 tests total
  - Typically 7,559 passed
  - ~49 skipped (doctests that require features not available in stage0)
  - 0 failed (clean baseline)

### Output Format
The test runner parses Rust's standard test output format:
```
test result: ok. 1816 passed; 0 failed; 2 ignored; 0 measured; 0 filtered out
```

And produces JSON output:
```json
{"passed": 7559, "failed": 0, "skipped": 49, "total": 7608}
```

## Additional Notes

### Time Efficiency
- **Setup time**: ~30 seconds (downloading stage0 compiler on first run, cached thereafter)
- **Test execution time**: ~2 minutes
- **Total time**: < 3 minutes per test run

### Commit Portability
The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They rely on:
- The x.py bootstrap system (stable interface)
- Standard test output format (unchanged between commits)
- Downloaded stage0 compiler (matches the branch, not specific commits)

### Known Limitations
1. **LLVM CI Downloads**: The bootstrap system attempts to download LLVM from CI, but these builds are often unavailable for older commits. The configuration explicitly disables this to avoid failures.

2. **Debug Assertions**: Stage0 compilers typically don't have debug assertions enabled, so we disable `rust.debug-assertions` in the config to avoid conflicts.

3. **Test Coverage**: The library/core tests are representative but don't cover:
   - Compiler tests (tests/ui, tests/codegen, etc.)
   - Full std library tests
   - Tool-specific tests (clippy, rustfmt, etc.)

   These were excluded to keep test time under 15 minutes. The core library tests still provide excellent coverage of fundamental functionality.

### Environment Cleanliness
- All build artifacts are created in the `/testbed/build/` directory (ignored by git)
- The `bootstrap.toml` configuration file is regenerated on each run (also ignored by git)
- `git status` remains clean after setup and test execution
- Build cache in `/testbed/build/cache/` is reused across runs for efficiency
