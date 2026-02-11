# Summary

This repository contains Conan, a C/C++ package manager written in Python. The testing setup validates the core package management functionality through a comprehensive unit test suite.

## System Dependencies

No system-level services are required for running the Conan test suite. The test environment uses:
- **Python**: Version 3.6+ (tested with 3.12.3)
- **CMake**: Version 3.15+ available in system PATH (for some integration tests)
- **Build tools**: GCC, Clang, and basic build-essential tools (pre-installed in the environment)

## Project Environment

The project uses a Python virtual environment to isolate dependencies:

- **Virtual Environment**: Created at `/testbed/.venv` (ignored by git)
- **PYTHONPATH**: Set to include `/testbed` directory for module imports
- **Package Installation**: Conan is installed in editable mode using `pip install -e .`
- **Dependencies**:
  - Runtime: requests, urllib3, colorama, PyYAML, Jinja2, etc. (from `conans/requirements.txt`)
  - Server: bottle, pluginbase, PyJWT (from `conans/requirements_server.txt`)
  - Development/Testing: pytest, pytest-xdist, mock, WebTest, parameterized, docker, paramiko (from `conans/requirements_dev.txt`)

## Testing Framework

- **Framework**: pytest (version 7+)
- **Test Location**: `/testbed/test/unittests/`
- **Test Count**: 1335 total tests (1324 passed, 11 skipped on successful run)
- **Execution Time**: Approximately 1-2 minutes for the full unit test suite
- **Test Types**: Unit tests covering:
  - CLI command parsing and execution
  - Client API functionality
  - Package model and versioning
  - Build tools integration (CMake, Autotools, Meson, etc.)
  - Server REST API endpoints
  - Configuration and profile management
  - File utilities and path handling

## Additional Notes

### Script Design
The three scripts work together as follows:
1. **setup_system.sh**: Minimal script that exits successfully (no system services needed)
2. **setup_shell.sh**: Creates/activates virtual environment, installs all dependencies, and sets PYTHONPATH
3. **run_tests**: Executes pytest on unit tests and parses output to JSON format

### Testing Strategy
The unit tests were chosen over integration/functional tests because:
- They run faster (1-2 minutes vs 10+ minutes)
- They are more deterministic (don't depend on external tools like git, svn, docker)
- They provide comprehensive coverage of core functionality
- They work reliably across different environments

### Portability
All scripts are designed to work on both the current commit (HEAD) and previous commit (HEAD~1) without modifications. They handle dependencies dynamically and don't hardcode version-specific information.

### Git Cleanliness
The setup process only creates/modifies files that are already in `.gitignore`:
- `.venv/` directory (virtual environment)
- `*.pyc` and `__pycache__/` (Python bytecode)
- `.pytest_cache/` (pytest cache)
- `*.egg-info/` (package metadata)

Running `git status` after setup shows a clean working tree with no modifications to tracked files.
