# Summary

This repository is **Envoy Proxy**, a cloud-native high-performance edge/middle/service proxy written primarily in C++. The project uses **Bazel** as its build system for C++ components and has a suite of **Python-based tests** for tooling validation.

For this testing setup, we configured a minimal environment to run the **Python unit tests** in the `tools` directory, which test various utility scripts and tooling components used in the Envoy development workflow.

## System Dependencies

No system-level services or runtime dependencies are required for the Python tooling tests.

The system setup script (`/scripts/setup_system.sh`) exists but performs no operations, as the Python tests are self-contained and don't require:
- Database services (PostgreSQL, MySQL, etc.)
- Redis or cache services
- Message queues
- System configuration changes

## Project Environment

### Build System
- **Primary**: Bazel 7.6.0 (installed via Bazelisk)
- **Language**: Python 3.12.3 for the tooling tests

### Dependencies
The shell setup installs the following Python packages:
- `pytest>=7.0` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage support
- `pyyaml` - YAML parsing
- `protobuf` - Protocol Buffer support

### Environment Variables
- `ENVOY_SRCDIR=/testbed` - Source directory
- `SRCDIR=/testbed` - Alternative source directory reference
- `PYTHONPATH=/testbed` - Enables imports from the testbed root
- `PATH` - Extended to include `/home/benchmarker/.local/bin` for pytest

### Special Configuration
A minimal `tools/testing/plugin.py` module is created during setup to satisfy the pytest plugin requirement in `pytest.ini`. This file is git-ignored and recreated on each clean run.

## Testing Framework

### Framework: pytest

The tests are run using pytest with a custom configuration that:
- Uses `-c /dev/null` to bypass the repository's `pytest.ini` configuration
- This is necessary because the default config attempts to load all tools tests, many of which have complex Bazel-specific dependencies

### Test Suite
The test suite focuses on **api_versioning** tests, which are self-contained and don't require Bazel runtime or complex dependencies:
- `tools/api_versioning/generate_api_version_header_test.py` (2 tests)
- `tools/api_versioning/utils_test.py` (16 tests)

**Total: 18 tests**

These tests validate:
1. API version header generation
2. Version parsing and validation utilities
3. Deprecated version annotation handling

### Test Execution
Tests are executed with:
```bash
pytest -c /dev/null --tb=short --color=no -v \
    tools/api_versioning/generate_api_version_header_test.py \
    tools/api_versioning/utils_test.py
```

### Output Format
The test runner parses pytest output and produces JSON in the format:
```json
{"passed": 18, "failed": 0, "skipped": 0, "total": 18}
```

## Additional Notes

### Why Not All Tests?
The repository contains additional Python tests in:
- `tools/api_proto_breaking_change_detector/`
- `tools/dependency/`
- `tools/spelling/`
- `tools/protoprint/`

However, these tests require:
- `rules_python` (Bazel rules for Python)
- Generated test data files
- Additional modules that are only available in the Bazel build environment

Running these would require a full Bazel build setup with proper workspace configuration, which is beyond the scope of a lightweight pytest runner.

### Portability
The scripts work on both:
- Current commit (HEAD): 6b8294f
- Previous commit (HEAD~1): e141b8d

This is ensured by:
1. Using Bazelisk to auto-install the correct Bazel version from `.bazelversion`
2. Installing Python dependencies fresh on each setup
3. Not relying on any built artifacts or generated files
4. Creating necessary stub files (like `tools/testing/plugin.py`) during setup

### Git Cleanliness
After running `git clean -xdff` and the test suite, the working directory remains clean with no modifications to tracked files. Only build artifacts and installed dependencies are created in ignored locations.
