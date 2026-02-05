# Summary

This repository contains the AWS CLI v2, a unified command line interface for Amazon Web Services. The test environment has been configured to run a representative subset of the project's unit tests using pytest with parallel execution.

## System Dependencies

No system-level services or packages are required for running the AWS CLI tests. The `/scripts/setup_system.sh` script exists but performs no operations as all dependencies can be installed at the project level.

## Project Environment

### Language and Runtime
- **Language**: Python
- **Supported Versions**: Python 3.8, 3.9, 3.10, 3.11 (as specified in pyproject.toml)
- **Selected Version**: Python 3.11.14 (highest supported version available in the environment)
- **Virtual Environment**: Created in `/testbed/.venv` using Python's built-in venv module

### Package Management
- **Build System**: flit_core (PEP 517 backend)
- **Package Manager**: pip
- **Installation Method**:
  1. Install base requirements (wheel, flit_core)
  2. Install all requirements including test dependencies (pytest, pytest-xdist, pytest-cov, etc.)
  3. Build wheel using `python -m build`
  4. Install built wheel package

### Key Dependencies
- **Core**: colorama, docutils, cryptography, ruamel.yaml, prompt-toolkit, awscrt, botocore, s3transfer
- **Testing**: pytest==7.2.0, pytest-xdist==3.1.0, pytest-cov==4.0.0
- **Build**: build==0.7.0, tox==4.4.12

## Testing Framework

### Test Runner
- **Framework**: pytest 7.2.0
- **Parallel Execution**: pytest-xdist with `--numprocesses=auto` (limited to 4 max processes)
- **Distribution Strategy**: `--dist=loadfile` (distributes tests by file for better load balancing)

### Test Scope
The `/scripts/run_tests` script runs a representative subset of unit tests including:
- Core utility tests (test_utils.py)
- CLI driver and argument processing tests
- Formatter, table, and text output tests
- All customization tests (unit/customizations/)

This subset represents approximately 3,092 tests covering the most critical functionality of the AWS CLI, completing in under 15 minutes.

### Test Execution
Tests are run from the `/testbed/tests` directory with the environment variable `TESTS_REMOVE_REPO_ROOT_FROM_PATH=true` set to ensure tests import from the installed package rather than the source directory.

### Output Format
The test runner outputs JSON to stdout in the format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Idempotency
The setup script is idempotent - it checks if dependencies are already installed before attempting to install them. Running `source /scripts/setup_shell.sh` multiple times is safe and will skip unnecessary installations on subsequent runs.

### Git Cleanliness
The setup process creates a `.venv` directory in `/testbed/` which is untracked by git but is properly handled by the project's .gitignore patterns. All other generated files (build/, dist/, __pycache__/) are also gitignored and won't appear as changes in `git status`.

### Test Selection Rationale
- The full test suite contains over 7,000 unit tests and additional functional/integration tests
- Running all tests would exceed the 15-minute time constraint
- The selected subset covers core CLI functionality, argument processing, output formatting, and AWS service customizations
- This provides good coverage of critical code paths while remaining within time constraints
- Integration tests are excluded as they may require AWS credentials and take longer to execute

### Environment Variables
The setup maintains shell environment compatibility by:
- Activating a virtual environment (sourced, not executed)
- Exporting PYTHON and PYTHON_VERSION variables
- Setting up proper PATH precedence for the venv

### Compatibility
The scripts are designed to work on both HEAD and HEAD~1 commits without modification, ensuring portability across different versions of the codebase.
