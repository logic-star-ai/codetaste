# Summary

This testing setup configures and runs Envoy proxy unit tests. Envoy is a high-performance C++ network proxy that uses the Bazel build system. The scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification.

## System Dependencies

- **Bazel 6.5.0**: Build system used by Envoy
- **lld**: LLVM linker required for building C++ dependencies
- **gcc 13.3.0**: C++ compiler (used instead of clang to avoid strict thread-safety warnings)
- **Standard development tools**: Already present in Ubuntu 24.04 environment

The system setup script (`/scripts/setup_system.sh`) installs the lld linker, which is required by Envoy's build process for linking external dependencies.

## Project Environment

**Language**: C++ (with Bazel build system)

**Build Configuration**:
- Compiler: GCC 13.3.0 (via `--config=gcc`)
- Build type: `fastbuild` (faster than optimized builds, includes debug symbols)
- TCMalloc: Disabled (via `--define tcmalloc=disabled`) to avoid compiler version incompatibilities
- Build directory: `~/.cache/envoy-bazel`

**Environment Variables**:
- `ENVOY_SRCDIR=/testbed`
- `NUM_CPUS=96` (auto-detected)
- `BUILD_DIR=~/.cache/envoy-bazel`
- `CC=gcc`, `CXX=g++`

**Special Configuration**:
The setup script patches `bazel/repository_locations.bzl` to fix a checksum mismatch in the googleurl dependency. The upstream storage has updated the file but the repository has not been updated yet. The actual checksum (`fc694942e8a7491dcc1dde1bddf48a31370a1f46fef862bc17acf07c34dc6325`) replaces the expected one.

## Testing Framework

**Framework**: Google Test (gtest) with Bazel test runner

**Test Subset**: The tests run a representative subset of core Envoy unit tests from `//test/common/...`:
- `//test/common/buffer/...` - Buffer management tests
- `//test/common/common/...` - Common utilities tests
- `//test/common/http/...` - HTTP protocol tests
- `//test/common/network/...` - Network layer tests
- `//test/common/stats/...` - Statistics/metrics tests

These tests cover fundamental functionality of the Envoy proxy without requiring full integration tests or extensive external dependencies.

**Test Execution**:
- Bazel runs tests in parallel (up to 96 CPUs)
- Tests use 80% of available RAM
- Test output is captured and parsed to extract pass/fail/skip counts
- Results are output in JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

**Challenges Encountered**:

1. **Dependency Checksum Mismatch**: The googleurl dependency has a checksum mismatch between the repository definition and the actual file in Google's storage. This is resolved by updating the checksum in `bazel/repository_locations.bzl` during setup.

2. **Compiler Compatibility**: Both Clang 18 and GCC 13 encountered issues with the default tcmalloc configuration:
   - Clang 18: Strict thread-safety warnings treated as errors
   - GCC 13: Symbol redefinition errors in tcmalloc headers

   Solution: Disabled tcmalloc using `--define tcmalloc=disabled`, which uses the system allocator instead.

3. **Build Time**: Initial builds take significant time (5-10 minutes) as Bazel downloads and compiles all dependencies. Subsequent builds are much faster due to caching.

**Script Portability**: All scripts are designed to work identically on HEAD and HEAD~1 without modifications. The scripts only modify files in ignored directories (build artifacts, bazel cache) and the checksum in `bazel/repository_locations.bzl` which is acceptable per the requirements.

**Deterministic Results**: Tests produce deterministic results assuming no environmental changes. The test suite includes unit tests that are designed to be hermetic and repeatable.
