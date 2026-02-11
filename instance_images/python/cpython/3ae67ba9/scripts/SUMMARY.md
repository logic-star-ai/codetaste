# Summary

This repository contains **CPython**, the reference implementation of the Python programming language (version 3.14.0a6+). The testing setup builds CPython from source and runs the official test suite using the `test` module.

## System Dependencies

The following system packages are required to build CPython:

- **Build tools**: `build-essential`, `pkg-config`, `ccache`, `gdb`
- **Libraries**:
  - `libb2-dev` - BLAKE2 cryptographic hash
  - `libbz2-dev` - bzip2 compression
  - `libffi-dev` - Foreign Function Interface
  - `libgdbm-dev`, `libgdbm-compat-dev` - GNU dbm database
  - `liblzma-dev`, `lzma`, `lzma-dev` - LZMA compression
  - `libncurses5-dev` - Terminal handling
  - `libreadline6-dev` - Command line editing
  - `libsqlite3-dev` - SQLite database
  - `libssl-dev` - OpenSSL cryptography
  - `tk-dev` - Tk GUI toolkit
  - `uuid-dev` - UUID generation
  - `zlib1g-dev` - zlib compression
- **Testing tools**: `strace`, `xvfb` (for headless GUI tests), `lcov` (coverage)

These dependencies are installed via APT package manager and are already available in the Ubuntu 24.04 environment.

## PROJECT Environment

### Build Configuration

CPython is built from source with the following configuration:

- **Configure flags**: `--with-pydebug --enable-slower-safety`
  - `--with-pydebug`: Enables debug mode with additional runtime checks
  - `--enable-slower-safety`: Enables additional safety checks

- **Build method**: Parallel build using `make -j$(nproc)` for optimal performance

### Build Process

The `setup_shell.sh` script performs the following:

1. Runs `./configure` with debug and safety flags
2. Builds CPython using parallel make
3. Sets environment variables:
   - `PYTHONPATH=/testbed/Lib`
   - `PATH=/testbed:$PATH`

The build is idempotent - if Python is already built, it skips the build step.

### Build Artifacts

The build produces:
- `/testbed/python` - The Python executable
- `/testbed/libpython3.14d.a` - Static library (debug build)
- `/testbed/build/` - Compiled extension modules
- Various `.pyc` bytecode cache files (git-ignored)

## Testing Framework

### Test Runner

CPython uses its built-in `test` module (located in `/testbed/Lib/test/`) as the testing framework. This is invoked as:

```bash
/testbed/python -m test [options]
```

### Test Execution

The `run_tests` script executes tests with the following parameters:

- **Test mode**: `--fast-ci` - Fast Continuous Integration mode (subset of tests suitable for CI)
- **Resource exclusions**: `-u-gui` - Excludes GUI tests (since we run in headless mode)
- **Parallelization**: `-j 4` - Runs 4 test worker processes in parallel
- **Timeout**: `--timeout 900` - 15 minute timeout per test file

### Test Statistics

The test suite outputs statistics in the format:
```
Total tests: run=X,XXX failures=YY skipped=Z,ZZZ
```

The `run_tests` script parses this output and generates JSON:
```json
{"passed": <passed_count>, "failed": <failed_count>, "skipped": <skipped_count>, "total": <total_count>}
```

Where:
- `total` = number of individual test cases run
- `failed` = number of test cases that failed
- `skipped` = number of test cases skipped
- `passed` = total - failed - skipped

### Representative Test Coverage

The `--fast-ci` mode runs approximately 485 test files covering:
- Core language features (builtin types, operators, syntax)
- Standard library modules
- C API and extension modules
- Concurrency and multiprocessing
- I/O and networking
- Platform-specific features (Unix/Linux)

Typical test run statistics:
- **Total test cases**: ~45,000
- **Test files**: ~485
- **Duration**: 12-15 minutes
- **Pass rate**: >99% (excluding flaky tests)

## Additional Notes

### Script Portability

All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work on both:
- The current commit (HEAD)
- The previous commit (HEAD~1)

This is achieved by:
1. Not hardcoding any commit-specific paths or values
2. Using the standard CPython build system (`./configure` and `make`)
3. Dynamically detecting whether a build already exists

### Known Test Variations

Some tests may occasionally fail or be skipped due to:

1. **Platform-specific tests**: Tests for Windows, macOS, iOS, Android are skipped on Linux
2. **Resource-intensive tests**: Some tests are skipped without special resources (e.g., `test_zipfile64`)
3. **Timing-dependent tests**: Tests like `test_perf_profiler` may occasionally fail due to timing issues
4. **Network tests**: Tests requiring network access (e.g., `test_smtpnet`) may be slow or unstable

### Git Cleanliness

The scripts are designed to maintain git cleanliness:
- All build artifacts are in git-ignored directories (`build/`, `*.pyc`, etc.)
- `git status` shows clean working tree after running scripts
- The scripts work correctly after `git clean -xdff`

### Performance Considerations

- **Parallel builds**: Uses all available CPU cores via `make -j$(nproc)`
- **Parallel tests**: Runs 4 test workers in parallel for faster execution
- **ccache**: Can be configured for faster rebuilds (though not used in current setup)
- **Build time**: ~2-3 minutes on modern hardware
- **Test time**: ~12-15 minutes for full `--fast-ci` suite
