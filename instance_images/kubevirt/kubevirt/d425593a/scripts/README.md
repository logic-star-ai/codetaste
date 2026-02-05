# KubeVirt Test Scripts

This directory contains scripts for setting up and running tests for the KubeVirt project.

## Files

- **setup_system.sh** - System-level setup (requires sudo). Currently a no-op as no system services are needed.
- **setup_shell.sh** - Shell environment setup. Sets environment variables and verifies Go installation.
- **run_tests** - Executes the test suite and outputs results in JSON format.
- **SUMMARY.md** - Detailed documentation of the testing setup.

## Usage

### Quick Start

```bash
# Clean environment and run tests
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

### Individual Steps

```bash
# 1. Clean the repository (removes build artifacts)
git clean -xdff

# 2. Setup system (currently no-op)
sudo /scripts/setup_system.sh

# 3. Setup shell environment (must be sourced)
source /scripts/setup_shell.sh

# 4. Run tests
/scripts/run_tests
```

## Output Format

The `run_tests` script outputs JSON on its final line:

```json
{"passed": 1065, "failed": 0, "skipped": 0, "total": 1065}
```

Where:
- `passed` - Number of test specifications that passed
- `failed` - Number of test specifications that failed
- `skipped` - Number of test specifications that were skipped
- `total` - Total number of test specifications run

## Test Coverage

The test suite runs approximately 33 Go packages covering:
- Core functionality (instancetype, container-disk, config)
- Storage management (types, snapshot, export)
- Operator functionality (resource generation, RBAC)
- Network management (cache, namescheme, link)
- Virtualization wrappers (virtwrap API, converter, device)
- Client libraries (kubecli, logging)

Total: ~1065 test specifications in ~5 minutes

## Requirements

- Go 1.19 or higher (tested with Go 1.23.4)
- No external dependencies or services required
- All dependencies are vendored in the repository

## Compatibility

These scripts are designed to work across different Git commits without modification.
They have been tested on both HEAD and HEAD~1 of the repository.
