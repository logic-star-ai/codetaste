# Test Environment Setup Scripts

This directory contains scripts to set up and run tests for the Sanity.io monorepo.

## Scripts

### /scripts/setup_system.sh
System-level configuration script run with sudo. Currently a no-op as no system services are required.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### /scripts/setup_shell.sh
Configures the shell environment and installs project dependencies. Must be sourced to set environment variables.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**What it does:**
- Installs npm dependencies via pnpm
- Builds all packages using Turbo
- Sets NODE_ENV=test
- Idempotent - safe to run multiple times

### /scripts/run_tests
Executes the Vitest test suite and outputs results in JSON format.

**Usage:**
```bash
/scripts/run_tests
```

**Output:**
Prints test results in JSON format as the final line of stdout:
```json
{"passed": 2146, "failed": 3, "skipped": 111, "total": 2272}
```

## Complete Workflow

To run tests from a clean state:

```bash
# Clean the repository (removes build artifacts, node_modules, etc.)
git clean -xdff

# Set up system (currently no-op)
sudo /scripts/setup_system.sh

# Set up shell environment and install dependencies
source /scripts/setup_shell.sh

# Run tests
/scripts/run_tests
```

## Notes

- All scripts work on both HEAD and HEAD~1 without modifications
- Scripts only modify files/directories ignored by git (node_modules/, lib/, etc.)
- Test execution takes approximately 80 seconds after setup
- Initial setup (install + build) takes 3-4 minutes on a clean checkout
- Total test count: ~2270 tests across multiple packages
