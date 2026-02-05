# Summary

This document describes the testing setup for OpenRCT2, an open-source re-implementation of RollerCoaster Tycoon 2 written in C++.

## System Dependencies

OpenRCT2 is a C++ project that requires various system-level libraries for graphics, audio, networking, and compression support. No system services (like databases or Redis) are required for the test suite.

The following system packages are installed via `apt`:
- **Build tools**: build-essential, cmake, ninja-build, pkg-config, ccache
- **Graphics libraries**: libsdl2-dev, libpng-dev, libfreetype6-dev, libfontconfig1-dev
- **Compression**: libzip-dev, zlib1g-dev
- **Networking/Security**: libssl-dev, libcurl4-openssl-dev
- **Audio**: libspeexdsp-dev, libflac-dev, libogg-dev, libvorbis-dev
- **Text/Localization**: libicu-dev
- **Testing**: libgtest-dev
- **Other**: nlohmann-json3-dev, git

## Project Environment

OpenRCT2 uses CMake as its build system with Ninja as the build tool. The project is configured with the following options:
- Build type: Release
- Tests enabled: ON
- Shared libraries: ON
- Portable mode: ON
- Discord RPC: Disabled (not needed for tests)
- Google Benchmark: Disabled (not needed for tests)
- Asset downloads: Disabled (tests use local data)

### Build Process
1. CMake configures the project in the `bin/` directory
2. Ninja compiles approximately 520 compilation units
3. The test binary `OpenRCT2Tests` is built along with the shared library `libopenrct2.so`
4. Symlinks are created from `bin/` to `data/` and `language/` directories for runtime access

### Environment Variables
- `CCACHE_DIR`: Set to `/tmp/ccache` for faster rebuilds
- `PATH`: Modified to include ccache for compiler caching

## Testing Framework

OpenRCT2 uses **Google Test (GTest)** as its testing framework.

### Test Execution
The test suite contains approximately 232 tests across 30 test suites covering:
- Core functionality (BitSet, CircularBuffer, String operations)
- Cryptography (SHA1, RSA)
- File I/O (Compression, Sawyer coding)
- Game logic (Pathfinding, Ride ratings)
- Import/Export (S6 format, park files)
- Localisation and formatting
- Tile elements and game state

### Test Results
Tests are executed by running the `OpenRCT2Tests` binary, which produces:
- XML output for detailed results
- Console output with pass/fail status
- JSON summary in the format: `{"passed": X, "failed": Y, "skipped": Z, "total": N}`

### Known Test Failures
Some tests (approximately 10 out of 232) fail due to missing language pack initialization. These tests require the complete data files that would normally be downloaded during installation but are not included in the repository. The failures are consistent and expected in the test environment without full asset downloads.

## Additional Notes

### Portability
The scripts have been designed to work across different commits. They successfully run on both the current HEAD and HEAD~1 without modifications.

### Build Time
- First build (from clean): ~2-3 minutes on a modern multi-core system
- Incremental builds: Much faster due to ccache
- Test execution: ~1 second for the full suite

### Memory and Disk Requirements
- The build directory (`bin/`) is approximately 200-300 MB
- ccache directory can grow to several hundred MB with repeated builds
- No special memory requirements beyond standard compilation needs

### Script Organization
- `/scripts/setup_system.sh`: Minimal script (no system services needed)
- `/scripts/setup_shell.sh`: Installs dependencies, configures, and builds the project
- `/scripts/run_tests`: Executes tests and formats output as JSON

The setup is idempotent - running `setup_shell.sh` multiple times will not reinstall packages or reconfigure unless forced via environment variables.
