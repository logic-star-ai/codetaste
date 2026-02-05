# Summary

This TensorFlow repository testing setup uses **Bazel 3.7.2** as the primary build system with **Python 3.11** and **GCC 11** for compatibility. The test framework attempts to build and run a subset of TensorFlow's data utility tests.

## System Dependencies

The testing environment requires the following system-level packages:

1. **Bazel 3.7.2** - Primary build and test orchestration tool
   - Installed from GitHub releases to `/usr/local/bin`
   - Required version specified in `.bazelversion` file

2. **GCC 11 / G++ 11** - C++ compiler toolchain
   - Installed via apt: `gcc-11 g++-11`
   - Required for compatibility with TensorFlow's dependencies
   - Newer GCC versions (14+) have compilation issues with this codebase

3. **Python 3.11** - Runtime environment
   - Installed via `uv` package manager
   - Required for protobuf compatibility (Python 3.12 has breaking changes)

4. **System Python packages**
   - `python3-dev`, `python3-pip` for development headers and package management
   - `python3-numpy` system package (installed via apt)

## Project Environment

### Build Configuration

The project uses a non-interactive configuration approach:
- **Build system**: Bazel with custom configuration (`.tf_configure.bazelrc`)
- **Build mode**: CPU-only, no CUDA/ROCM support
- **API version**: TensorFlow 2.x (TF2_BEHAVIOR=1)
- **Optimization**: `-march=native -Wno-sign-compare`

### Python Dependencies

The following Python packages are installed per Python 3.11:
- `numpy` - Numerical computing library
- `absl-py` - Abseil Python library
- `six` - Python 2/3 compatibility
- `wrapt` - Object proxy library
- `protobuf` - Protocol buffers

These are installed to either system packages (with `--break-system-packages`) or user site-packages as fallback.

### Environment Variables

- `PYTHON_BIN_PATH`: Path to Python 3.11 interpreter
- `PYTHON_LIB_PATH`: Python site-packages directory
- `CC`/`CXX`: Set to gcc-11/g++-11
- `TF2_BEHAVIOR`: Set to 1 for TensorFlow 2.x behavior
- `TEST_TMPDIR`: Bazel test temporary directory

## Testing Framework

### Framework: Bazel Test

TensorFlow uses Bazel's built-in test framework (`bazel test`) to run Python tests. Test targets are defined in BUILD files throughout the repository.

### Test Selection

The test suite runs a small subset of TensorFlow's data utility tests:
- `//tensorflow/python/data/util:options_test`
- `//tensorflow/python/data/util:random_seed_test`

These tests were selected as representative samples of TensorFlow's Python testing infrastructure.

### Test Execution

Tests are executed with:
- 10-minute timeout per test
- Detailed test summaries
- Verbose failure reporting
- Keep-going mode (continue on failures)

### Output Format

The test script outputs a single JSON line:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Compilation Compatibility Issues

This TensorFlow snapshot (commit 98a2d7d1) has **fundamental compilation compatibility issues** with modern development environments:

1. **Missing C++ includes**: Multiple dependencies (LLVM, protobuf, absl, TFLite) are missing required `#include` directives (e.g., `<cstdint>`) that are mandatory in C++17 and later.

2. **Python 3.12 incompatibility**: The bundled protobuf version has incompatibilities with Python 3.12's internal API changes (PyFrameObject structure).

3. **GCC version sensitivity**: Code compiles poorly with GCC 14+ due to stricter standards compliance.

### Workarounds Applied

- **Python version**: Downgraded to Python 3.11 for protobuf compatibility
- **Compiler version**: Using GCC 11 instead of default GCC 14
- **Test selection**: Limited to specific test targets to minimize build surface

### Test Results

Due to the compilation issues described above:
- Most tests **fail to build** rather than fail at runtime
- The test framework correctly reports these build failures
- The scripts are portable and work on both HEAD and HEAD~1

### Script Portability

All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) are:
- ✅ Portable across HEAD and HEAD~1
- ✅ Idempotent (safe to run multiple times)
- ✅ Non-destructive to version-controlled files
- ✅ Produce deterministic JSON output

The scripts document the build environment requirements and attempt compilation, accurately reporting failures when they occur.
