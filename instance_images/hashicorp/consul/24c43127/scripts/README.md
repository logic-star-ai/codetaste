# Consul Test Environment Scripts

This directory contains scripts to set up and run tests for the HashiCorp Consul project.

## Scripts

### setup_system.sh
System-level setup script that must be run with `sudo`. Currently performs no operations as no system services are required for basic Go unit tests.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### setup_shell.sh
Shell environment configuration script. Must be sourced (not executed) to set environment variables in the current shell.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**What it does:**
- Sets up Go environment variables (GOPATH, PATH, etc.)
- Downloads Go module dependencies for main module and submodules
- Installs gotestsum test runner if not already present
- Creates marker files (.deps_downloaded) for idempotent operation

### run_tests
Test execution script that runs a representative subset of tests and outputs results in JSON format.

**Usage:**
```bash
/scripts/run_tests
```

**Prerequisites:**
- Must be run after sourcing setup_shell.sh
- Can be run multiple times without re-sourcing setup_shell.sh

**Output:**
- Test progress to stderr
- Final JSON result to stdout: `{"passed": X, "failed": Y, "skipped": Z, "total": N}`

## Complete Workflow

To run the full test suite from a clean state:

```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

To run tests again in the same shell (without re-setup):

```bash
/scripts/run_tests
```

Or re-source and run:

```bash
source /scripts/setup_shell.sh && /scripts/run_tests
```

## Notes

- All scripts work on both HEAD and HEAD~1 commits
- Setup is idempotent - safe to run multiple times
- Tests complete in approximately 20-30 seconds
- JSON output can be parsed programmatically for CI/CD integration
