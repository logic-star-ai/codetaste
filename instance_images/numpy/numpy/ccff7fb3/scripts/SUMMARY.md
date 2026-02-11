# Summary

This repository contains NumPy, a fundamental package for scientific computing with Python. The testing setup builds NumPy from source using the meson build system and runs a comprehensive test suite using pytest.

## System Dependencies

No system services are required for NumPy testing. The following system-level packages are pre-installed and used:
- GCC 13 (C compiler)
- G++ 13 (C++ compiler)
- Python 3.11.14 (installed via uv)
- Standard build tools (make, ninja)

Note: Fortran compiler is not required for building NumPy itself, though f2py tests will be skipped without one.

## Project Environment

### Python Version
- Python 3.11.14 (from /opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11)
- NumPy requires Python >= 3.10

### Virtual Environment
- Location: /tmp/numpy_venv
- Created and managed by setup_shell.sh
- Persists across test runs for efficiency

### Build System
- Build system: Meson + Ninja
- Build wrapper: spin (NumPy's development CLI tool)
- Build directory: /testbed/build
- Install directory: /testbed/build-install

### Key Dependencies
- meson-python >= 0.15.0 (build backend)
- Cython >= 3.0.6 (for C extensions)
- ninja (build tool)
- spin 0.8 (development CLI)
- scipy-openblas32 0.3.27.44.3 (BLAS/LAPACK implementation)
- pytest 7.4.0 (test runner)
- hypothesis 6.81.1 (property-based testing)
- pytest-xdist (parallel test execution)
- pytest-cov 4.1.0 (coverage)

### Git Submodules
NumPy uses git submodules for vendored dependencies:
- vendored-meson/meson (Meson build system)
- numpy/_core/src/common/pythoncapi-compat
- numpy/_core/src/highway
- numpy/_core/src/npysort/x86-simd-sort
- numpy/_core/src/umath/svml
- numpy/fft/pocketfft

These are automatically initialized by setup_shell.sh.

## Testing Framework

### Test Runner
- Framework: pytest 7.4.0
- Parallel execution: pytest-xdist with `-n auto` (uses all available CPU cores)
- Test marker: `-m "not slow"` (excludes slow tests for faster execution)

### Test Execution
Tests are run from /tmp directory (not /testbed) to avoid import conflicts with the source code. The built NumPy is accessed via PYTHONPATH pointing to /testbed/build-install/usr/lib/python3.11/site-packages.

### Test Results
The test suite runs approximately 49,000+ tests in ~50-60 seconds with the following typical results:
- Passed: ~48,100+ tests
- Failed: ~4 tests (known issues with distutils imports)
- Skipped: ~955 tests
- Total: ~49,061 tests

### JSON Output Format
The run_tests script outputs test results in the following JSON format:
```json
{"passed": 48102, "failed": 4, "skipped": 955, "total": 49061}
```

## Additional Notes

### Build Notes
- The build process compiles NumPy with optimizations for multiple CPU architectures (SSE, AVX2, AVX512, etc.)
- SIMD optimizations are automatically detected and used based on available CPU features
- The build uses scipy-openblas32 for BLAS/LAPACK operations
- Warnings are not treated as errors to avoid build failures on compiler-specific warnings

### Test Compatibility
The scripts are designed to work on both the current commit (HEAD) and previous commit (HEAD~1) without modifications. This ensures that the testing infrastructure is robust and version-agnostic.

### Caching Strategy
The setup_shell.sh script uses marker files (/tmp/numpy_venv/.deps_installed and /tmp/numpy_venv/.numpy_built) to avoid redundant installations and builds. However, the git clean -xdff command in the test workflow removes build artifacts from /testbed, triggering a fresh build each time.

### Known Test Failures
Some tests consistently fail due to:
- distutils module import errors (deprecated in Python 3.12+)
- Module import issues in test_public_api tests

These are not related to the core NumPy functionality and are expected in the current development version.
