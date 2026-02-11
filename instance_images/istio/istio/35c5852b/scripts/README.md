# Testing Scripts for Istio

This directory contains the testing infrastructure scripts for the Istio project.

## Scripts

### /scripts/setup_system.sh
System-level setup script that runs with sudo privileges. For Istio unit tests, this is a no-op as no system services are required.

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### /scripts/setup_shell.sh
Shell environment configuration script that must be sourced (not executed). Sets up Go environment variables, installs dependencies, and prepares the build environment.

**Usage:**
```bash
source /scripts/setup_shell.sh
```

**What it does:**
- Sets Go module environment variables (GO111MODULE, GOPROXY, GOSUMDB)
- Configures GOPATH and GOBIN
- Creates necessary output directories
- Downloads Go module dependencies
- Installs go-junit-report tool

### /scripts/run_tests
Test execution script that runs a representative subset of unit tests and outputs results in JSON format.

**Usage:**
```bash
/scripts/run_tests
```

**Output Format:**
```json
{"passed": 2759, "failed": 16, "skipped": 2, "total": 2777}
```

**Test Packages:**
- ./pkg/config/...
- ./pkg/bootstrap/...
- ./pkg/kube/...
- ./pkg/util/...
- ./galley/pkg/config/...
- ./istioctl/pkg/...

## Complete Test Pipeline

To run the complete test pipeline from a clean state:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Requirements

- Go 1.23.4 (or compatible version >= 1.13)
- Git
- Standard Linux utilities (bash, etc.)

## Notes

- All scripts are designed to work on both HEAD and HEAD~1 without modification
- Scripts only modify gitignored files (out/, Go cache)
- `git status` will show a clean working tree after execution
- Test execution takes 2-3 minutes on first run, <1 minute with cached dependencies
