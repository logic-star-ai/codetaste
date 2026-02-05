# Testing Scripts for Cosmos SDK

This directory contains scripts to set up and run tests for the Cosmos SDK repository.

## Scripts Overview

### setup_system.sh
- **Purpose**: System-level configuration (run with sudo)
- **Usage**: `sudo /scripts/setup_system.sh`
- **Description**: Configures system services. Currently no services are needed for Cosmos SDK unit tests, so this script just exits successfully.

### setup_shell.sh  
- **Purpose**: Shell environment configuration and dependency installation
- **Usage**: `source /scripts/setup_shell.sh`
- **Description**: 
  - Downloads Go module dependencies for main module and all sub-modules
  - Installs tparse tool for better test output
  - Must be sourced to set up the environment correctly

### run_tests
- **Purpose**: Execute test suite and output JSON results
- **Usage**: `/scripts/run_tests`
- **Description**:
  - Runs a representative subset of core unit tests
  - Outputs JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`
  - Takes approximately 2-3 minutes to complete

## Complete Workflow

```bash
# Clean the repository
git clean -xdff

# Run system setup (with sudo)
sudo /scripts/setup_system.sh

# Set up shell environment (must be sourced)
source /scripts/setup_shell.sh

# Run tests
/scripts/run_tests
```

## One-liner
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Notes

- Scripts work on both HEAD and HEAD~1 commits without modification
- Git working tree remains clean after setup and testing
- All dependencies are installed outside /testbed
- Scripts are idempotent and can be run multiple times safely
