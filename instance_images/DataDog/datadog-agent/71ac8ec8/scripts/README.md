# Test Scripts for Datadog Agent

This directory contains scripts for setting up and running tests for the Datadog Agent repository.

## Scripts

### `/scripts/setup_system.sh`
System-level setup script that must be run with `sudo`. Currently performs no operations as no system services are required for unit tests.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### `/scripts/setup_shell.sh`
Shell environment setup script that configures the development environment. Must be sourced (not executed).

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**What it does:**
- Sets up Go environment variables (GOPATH, PATH)
- Creates Python virtual environment with required dependencies
- Installs invoke, requests, pyyaml, GitPython, and other Python tools
- Downloads Go module dependencies
- Validates Go and Python versions

### `/scripts/run_tests`
Executes a representative subset of Go unit tests and outputs results in JSON format.

**Usage:**
```bash
/scripts/run_tests
```

**Output:**
The script outputs test results with the last line being a JSON object:
```json
{"passed": 363, "failed": 2, "skipped": 2, "total": 367}
```

## Complete Test Run

To run the full test pipeline from a clean state:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Notes

- Scripts are designed to be idempotent - safe to run multiple times
- Python virtual environment is created at `/testbed/venv`
- Go dependencies are cached by Go's module system
- Tests complete in ~8-10 minutes
- Works on both HEAD and HEAD~1 commits without modification

## Test Selection

The test runner automatically discovers and runs tests from the first 100 packages in `./pkg/...` that contain test files. Tests are run with:
- `-short` flag to skip long-running integration tests
- `-v` flag for verbose output
- `10m` timeout per package
- CGO enabled for native code compilation

See `/scripts/SUMMARY.md` for detailed documentation.
