# Summary

This repository contains Money Manager Ex (MMEX), a cross-platform personal finance application written in C++ using wxWidgets GUI toolkit and CMake build system. The project does not have a traditional test suite; instead, the validation is done through successful compilation of the project.

## System Dependencies

The following system packages are required:
- **Build tools**: cmake, build-essential, ccache, pkg-config
- **Core libraries**: libssl-dev, libcurl4-openssl-dev, libgtk-3-dev, liblua5.3-dev
- **wxWidgets**: libwxgtk3.2-dev, libwxgtk-webview3.2-dev, libwxgtk-media3.2-dev (system packages from Ubuntu 24.04)
- **Utilities**: gettext, git, lsb-release, file, python3, python3-pip, appstream, wget, unzip

Key decision: We use the system-provided wxWidgets 3.2 packages instead of building from source, as Ubuntu 24.04 provides wxWidgets 3.2 with full webview support (webkit2gtk-4.1), which is compatible with the project requirements.

## PROJECT Environment

The project requires:
1. **Git submodules initialization**: The database schema and other dependencies are stored in git submodules that must be initialized before building
2. **Database header generation**: Python scripts (`sqlite2cpp.py` and `sqliteupgrade2cpp.py`) generate C++ headers from SQL schema files before compilation
3. **CMake build system**: The project uses CMake with Release build type
4. **ccache**: Build cache is enabled to speed up subsequent builds

Environment variables:
- `PATH`: Prepended with `/usr/lib/ccache` for build caching
- `CCACHE_DIR`: Set to `/tmp/.ccache` for cache storage

## Testing Framework

This project **does not have a traditional test suite**. The "test" consists of:
1. Generating database headers from SQL schemas
2. Configuring the project with CMake
3. Building the entire project with all 124 C++ source files

Success criteria:
- All source files compile without errors
- The main executable (`mmex`) is successfully built

The test output reports:
- **passed**: Number of successfully compiled source files (124)
- **failed**: Number of source files that failed to compile (0 on success)
- **skipped**: Always 0 (no skipping mechanism)
- **total**: Total number of C++ source files (124)

## Additional Notes

### Obstacles Encountered

1. **wxWidgets webview support**: Initially attempted to build wxWidgets 3.1.7 from source with webview support, but encountered compatibility issues with webkit2gtk-4.1 (the version available in Ubuntu 24.04). The older wxWidgets 3.1.x requires webkit2gtk-4.0, which is not available.

2. **Solution**: Switched to using system-provided wxWidgets 3.2 packages (libwxgtk3.2-dev), which have full compatibility with webkit2gtk-4.1 and include webview support out of the box.

3. **Git submodules**: The database directory is a git submodule that must be initialized before building. This is handled automatically in the setup script.

4. **Generated headers**: The build requires Python scripts to generate C++ headers from SQL schema files. This preprocessing step is essential and is performed in the `run_tests` script before CMake configuration.

### Script Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification. The scripts:
- Do not hardcode version-specific paths
- Use system packages rather than building dependencies from source (where possible)
- Initialize git submodules dynamically
- Generate database headers as part of the build process

### Performance

- Initial setup (with apt package installation): ~30-60 seconds
- First build: ~2-3 minutes (with ccache)
- Subsequent builds: Much faster due to ccache
- No system services are required (setup_system.sh is a no-op)
