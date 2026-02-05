# Netty Test Scripts

This directory contains the testing infrastructure for the Netty project.

## Files

- **setup_system.sh**: System-level setup (no-op for this project)
- **setup_shell.sh**: Shell environment configuration and dependency installation
- **run_tests**: Test execution script with JSON output
- **SUMMARY.md**: Comprehensive documentation of the testing setup

## Usage

To run the complete test suite from a clean state:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Expected Output

The test run will produce JSON output in the format:
```json
{"passed": 2369, "failed": 0, "skipped": 0, "total": 2369}
```

## Test Duration

- Setup: ~2-3 minutes
- Test execution: ~7-8 minutes
- Total: ~10 minutes

## Modules Tested

- common
- buffer
- codec
- codec-http
- transport
- handler
- resolver

Total: 2,369 tests across 7 core modules
