# Summary

This repository contains Endless Sky, a space exploration game written in C++. The project uses CMake as its build system and Catch2 as its unit testing framework.

## System Dependencies

The following packages are installed via apt:
- **Build tools**: g++, cmake, ninja-build, curl, git, pkg-config
- **Graphics libraries**: libgl1-mesa-dev, libglew-dev, libgles2-mesa-dev, libglu1-mesa-dev, libegl1-mesa-dev, libosmesa6, mesa-utils, libglvnd-dev
- **Window/input libraries**: libsdl2-dev, libxmu-dev, libxi-dev, libwayland-dev, libxkbcommon-dev, x11-utils
- **Image libraries**: libpng-dev, libjpeg-dev
- **Audio library**: libopenal-dev, libmad0-dev
- **Other libraries**: uuid-dev, libltdl-dev
- **Testing framework**: catch2

The sound card is disabled in the VM by configuring ALSA to use a null output to prevent audio-related issues during testing.

## Project Environment

- **Language**: C++ (C++20 standard required)
- **Build System**: CMake 3.19+ (uses presets)
- **Build Configuration**: Linux preset with system libraries (`-DES_USE_VCPKG=OFF -DES_USE_SYSTEM_LIBRARIES=ON`)
- **Build Mode**: Debug (includes sanitizers: address, undefined, etc.)
- **Build Generator**: Ninja Multi-Config
- **Build Directory**: `/testbed/build/linux`
- **Binary Output**: `/testbed/build/linux/Debug/endless-sky` (game), `/testbed/build/linux/tests/Debug/endless-sky-tests` (tests)

## Testing Framework

- **Framework**: Catch2 (v3.0+)
- **Test Executable**: `/testbed/build/linux/tests/Debug/endless-sky-tests`
- **Test Count**: 81 unit test cases with 76,593+ assertions
- **Test Categories**:
  - Unit tests covering: comparators, account, angle, bitset, category lists, conditions, datafile parsing, format, text layout, and more
  - Integration tests (discovered but not run in this setup - they require the full game executable)
- **Reporting**: Tests are run with XML reporter to extract individual test case results

The test script runs the unit tests directly via the Catch2 test executable and parses XML output to count passed/failed/skipped tests.

## Additional Notes

- The project uses sanitizers (ASan, UBSan, etc.) in Debug builds which helps catch memory and undefined behavior issues
- vcpkg is available but not used in this setup; system libraries are preferred for faster builds
- The build takes about 3-5 minutes on first run but is cached appropriately
- Integration tests exist but require running the actual game binary with specific configurations - these are not included in the current test suite
- The setup is idempotent - running `/scripts/setup_shell.sh` multiple times is safe
- All scripts work on both HEAD and HEAD~1 commits as required
