# Summary

This repository contains PPSSPP, a fast and portable PSP emulator written in C++. The testing setup builds and executes the project's unit tests using CMake.

## System Dependencies

The following system packages are required:
- **Build tools**: `cmake`, `build-essential` (gcc/g++/clang), `git`, `python3`, `wget`
- **SDL2**: `libsdl2-dev`, `libsdl2-ttf-dev` (for graphics and input)
- **OpenGL**: `libgl1-mesa-dev`, `libglu1-mesa-dev` (for GPU rendering)
- **Other libraries**: `libfontconfig1-dev` (font configuration)

FFmpeg is built from the internal git submodule rather than using system packages to avoid version compatibility issues.

## PROJECT Environment

### Language and Build System
- **Primary Language**: C++17
- **Build System**: CMake (minimum version 3.16)
- **Compiler**: Clang (as used in CI for better compatibility)

### Git Submodules
The project requires multiple git submodules to be initialized:
- `ext/armips`, `ext/cpu_features`, `ext/glslang`, `ext/SPIRV-Cross`
- `ext/native`, `ext/libchdr`, `ext/zstd`, `ext/miniupnp`
- `ext/rapidjson`, `ext/rcheevos`, `ext/naett`, `ext/libadrenotools`
- `ext/lua`, `ext/discord-rpc`, `ext/OpenXR-SDK`
- `ffmpeg` (built internally using `./linux_x86-64.sh`)

### Build Configuration
- **Build Mode**: Headless (HEADLESS=ON) - avoids GUI dependencies
- **Unit Tests**: Enabled (UNITTEST=ON)
- **Build Directory**: `build/` in the repository root
- **Parallel Build**: Uses all available CPU cores via `make -j$(nproc)`

## Testing Framework

### Test Binary
The unit tests are built into a single executable: `build/PPSSPPUnitTest`

### Test Execution
Tests are run with the `ALL` parameter: `./build/PPSSPPUnitTest ALL`

This executes all available unit tests, which include:
- Architecture-specific emitter tests (ARM, ARM64, x64, RISC-V)
- Vertex JIT tests
- Math utility tests (trigonometry, VFPU functions)
- Parser and IR optimization tests
- Memory map tests
- Shader generator tests
- Software GPU JIT tests
- Various utility and helper tests

### Test Results
- **Total Tests**: 36
- **Output Format**: JSON with counts of passed, failed, skipped, and total tests
- **Success Criteria**: All tests passing (exit code 0)

## Additional Notes

### Build Time
The initial build (including submodule initialization and FFmpeg compilation) takes approximately 5-10 minutes depending on available CPU cores. Subsequent builds with an existing build directory are much faster due to incremental compilation.

### Portability
The scripts are designed to work across commits (tested on HEAD and HEAD~1). The setup is portable and idempotent - running `setup_shell.sh` multiple times will skip already-completed steps.

### Architecture Support
The unit tests include architecture-specific code that may be conditionally compiled based on the host system (x86_64, ARM, ARM64, etc.). The current setup is tested on x86_64 Linux.

### Known Limitations
- Some optional dependencies (GLEW, Snappy, libzip) are not installed as they are not required for unit tests
- The headless build mode is used to avoid X11/Wayland display requirements during testing
