# Summary

This repository contains Apache Pegasus, a distributed key-value storage system written in C++. The test environment has been configured to build the project from source (including thirdparty dependencies) and run a representative subset of unit tests.

## System Dependencies

The following system packages are required and have been installed:

- **Build Tools**: build-essential, cmake, ccache, automake, libtool
- **Compilers**: gcc/g++, clang-14, llvm-14-dev
- **Java**: openjdk-8-jdk (required for building thirdparty dependencies)
- **Libraries**: libssl-dev, libaio-dev, zlib1g-dev, libkrb5-dev, libsasl2-dev
- **Utilities**: git, wget, curl, patch, netcat-openbsd, gdb, maven, flex, bison
- **Thrift**: Apache Thrift 0.11.0 (compiled from source and installed globally)

## Project Environment

The project uses:

- **Primary Language**: C++ (with CMake build system)
- **Build System**: CMake 3.24+ with custom run.sh wrapper script
- **Thirdparty Dependencies**: Managed via ExternalProject_Add in thirdparty/CMakeLists.txt
  - Key dependencies: Boost, RocksDB, gRPC, Abseil, S2 Geometry, and many others
  - Built once and cached in `/testbed/thirdparty/output`
- **Test Framework**: Google Test (GTest) with XML output

### Key Environment Variables

- `THIRDPARTY_ROOT`: Points to `/testbed/thirdparty`
- `BUILD_ROOT_DIR`: Points to `/testbed/build`
- `BUILD_LATEST_DIR`: Points to `/testbed/build/latest` (symlink to current build)
- `LD_LIBRARY_PATH`: Includes paths to thirdparty libraries and Java libraries
- `JAVA_HOME`: Set to `/usr/lib/jvm/java-8-openjdk-amd64`

## Testing Framework

### Test Structure

Pegasus uses Google Test (gtest) framework with tests organized into modules:

- **Unit Tests**: `pegasus_unit_test`, `dsn_utils_tests`, `dsn_runtime_tests`, etc.
- **Integration Tests**: Tests that require ZooKeeper or onebox cluster (not included in fast subset)
- **Test Output**: XML files in GTest format, saved to `$REPORT_DIR`

### Test Execution

The test suite is executed via `/scripts/run_tests` which:

1. Runs a representative subset of tests (7 modules) that complete in ~15 minutes
2. Selected tests cover core functionality without requiring cluster setup:
   - `base_test`: Basic functionality tests
   - `dsn_utils_tests`: Utility library tests
   - `dsn_runtime_tests`: Runtime system tests
   - `dsn_http_test`: HTTP server tests
   - `dsn_client_test`: Client library tests
   - `dsn_aio_test`: Async I/O tests
   - `pegasus_unit_test`: Main Pegasus unit tests

3. Parses XML output to extract pass/fail/skip counts
4. Outputs JSON summary: `{"passed": N, "failed": M, "skipped": K, "total": T}`

### Build Process

1. **Thirdparty Build**: ~30-60 minutes on first run (cached thereafter)
   - Downloads and compiles all dependencies
   - Some packages may warn/fail but essential ones succeed

2. **Pegasus Build**: ~20-40 minutes on first run (cached thereafter)
   - Generates thrift files
   - Compiles all C++ source with tests enabled
   - Creates test binaries in `build/latest/bin/`

## Additional Notes

### Challenges Encountered

1. **Thirdparty Build Complexity**: The thirdparty CMake build includes ~20+ external projects. Some non-essential packages may fail to build, but the build continues and essential dependencies succeed.

2. **Thrift Binary Location**: Pegasus expects thrift at `/testbed/thirdparty/output/bin/thrift` but we installed it globally. The `setup_shell.sh` script creates a symlink to bridge this gap.

3. **Build Time**: Full build (thirdparty + Pegasus) takes significant time (~1-2 hours on first run). The scripts are designed to be idempotent and skip rebuilding if artifacts already exist.

4. **Test Dependencies**: Some tests require ZooKeeper or a full onebox cluster. The test subset was chosen to avoid these dependencies while still providing good coverage.

### Script Portability

The scripts are designed to work on both HEAD and HEAD~1 commits by:
- Using the project's own `run.sh` build script (version-independent)
- Not modifying any versioned files in `/testbed/`
- Building artifacts in git-ignored directories (`build/`, `thirdparty/build/`, `thirdparty/output/`)
- Using standard test execution patterns that have been stable across versions

### Performance Considerations

- Parallel builds use `$(nproc)` to utilize all available CPU cores
- ccache is installed to speed up incremental builds
- Test subset selected to balance coverage with execution time
