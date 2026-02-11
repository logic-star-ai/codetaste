# Summary

This test environment is configured for Apache Arrow C++ unit tests. The setup builds and tests the core Arrow C++ library with minimal dependencies to ensure fast execution while still providing representative test coverage.

## System Dependencies

The following system packages are required and should be pre-installed:

- **Build Tools**: cmake (≥3.16), ninja-build, g++, gcc
- **Development Libraries**:
  - libboost-system-dev (for Boost system library support)
  - libutf8proc-dev (for UTF-8 string processing)
  - rapidjson-dev (for JSON parsing)

These are installed via `apt-get` in the Ubuntu 24.04 environment.

## Project Environment

### Build Configuration

The Apache Arrow C++ library is built with the following configuration:

- **Build Type**: Release (for faster execution)
- **Build Directory**: `/tmp/arrow-build/cpp`
- **Install Directory**: `/tmp/arrow-install`
- **Generator**: Ninja (for parallel builds)

### Arrow Features Enabled

The build enables a minimal but representative set of features:
- Core Arrow library
- Compute functions (ARROW_COMPUTE=ON)
- CSV reader/writer (ARROW_CSV=ON)
- JSON reader/writer (ARROW_JSON=ON)
- Filesystem interface (ARROW_FILESYSTEM=ON)
- UTF-8 processing support (ARROW_WITH_UTF8PROC=ON)
- Regular expression support (ARROW_WITH_RE2=ON)

### Arrow Features Disabled

To reduce build time and dependencies, the following are disabled:
- Parquet, ORC (columnar formats)
- Flight, Gandiva (RPC and expression compiler)
- Cloud storage (S3, GCS, Azure)
- Compression libraries (Brotli, BZ2, LZ4, Snappy, Zlib, Zstd)
- Alternative allocators (jemalloc, mimalloc)
- Dataset API, Acero query engine
- HDFS support

### Environment Variables

Key environment variables set by the setup:
- `ARROW_HOME`: Installation prefix
- `ARROW_TEST_DATA`: Path to test data files
- `PARQUET_TEST_DATA`: Path to Parquet test data
- `LD_LIBRARY_PATH`: Includes Arrow library path
- `AWS_EC2_METADATA_DISABLED`: Prevents AWS metadata lookups
- `ARROW_DEBUG_MEMORY_POOL`: Enables memory debugging

## Testing Framework

### Test Execution

- **Framework**: CTest (CMake's testing framework)
- **Test Label**: `unittest` (filters to unit tests only)
- **Parallelism**: Uses all available CPU cores via `$(nproc)`
- **Timeout**: 300 seconds (5 minutes) per test
- **Test Count**: ~51 unit tests in the minimal configuration

### Test Output

The `run_tests` script produces JSON output in the format:
```json
{"passed": N, "failed": M, "skipped": 0, "total": T}
```

Where:
- `passed`: Number of tests that passed
- `failed`: Number of tests that failed
- `skipped`: Number of skipped tests (always 0 for CTest)
- `total`: Total number of tests executed

### Expected Test Results

On a clean build, the test suite typically shows:
- **Total tests**: ~51 unit tests
- **Typical pass rate**: ~96% (49/51 tests)
- **Known failures**: 2 tests may fail due to timing or metadata compatibility issues:
  - `arrow-compute-scalar-temporal-test`
  - `arrow-ipc-read-write-test`

These failures are consistent across HEAD and HEAD~1, suggesting they are environmental or configuration-related rather than code defects.

## Additional Notes

### Build Performance

- **Build Time**: Approximately 3-5 minutes on modern hardware
- **Test Time**: Approximately 5-6 seconds for the full unit test suite
- **Disk Space**: Build artifacts consume approximately 500MB-1GB

### Idempotency

The `setup_shell.sh` script is idempotent and checks for a `.build_complete` marker file. If the build is already complete, it skips the rebuild process.

### Portability

All scripts work correctly on both HEAD and HEAD~1 commits without modification, as they reference relative paths and use BUNDLED dependency sources which are committed to the repository.

### Caching Strategy

The build directory (`/tmp/arrow-build`) and install directory (`/tmp/arrow-install`) are placed in `/tmp` to be easily cleaned between test runs. The `.build_complete` marker enables re-running tests without rebuilding.

### Dependencies Management

The build uses `ARROW_DEPENDENCY_SOURCE=BUNDLED` to fetch and build third-party dependencies (like re2, boost, xsimd, gflags) automatically during the CMake configuration phase. This ensures reproducibility across different environments.

### Git Cleanliness

After running the complete test sequence (`git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests`), the git working directory remains clean with no modifications to tracked files, as all build artifacts are placed outside `/testbed/`.
