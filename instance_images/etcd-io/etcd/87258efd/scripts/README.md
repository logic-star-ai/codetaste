# etcd Test Environment Scripts

This directory contains scripts to set up and run tests for the etcd repository.

## Scripts

### /scripts/setup_system.sh
System-level setup script that must be run with sudo privileges.
- Currently a no-op (exits 0) as etcd unit tests don't require system services
- Can be extended to start databases, Redis, or configure system limits if needed

**Usage:**
```bash
sudo /scripts/setup_system.sh
```

### /scripts/setup_shell.sh
Shell environment setup script that configures the development environment.
- Installs gobin tool (required by etcd build system)
- Downloads Go module dependencies
- Builds etcd binaries (etcd and etcdctl)

**Usage:**
```bash
source /scripts/setup_shell.sh
```

### /scripts/run_tests
Test execution script that runs the test suite and outputs results in JSON format.
- Runs unit tests for core etcd modules
- Outputs test results as a single JSON line: `{"passed": N, "failed": N, "skipped": N, "total": N}`
- Completes within 15 minutes

**Usage:**
```bash
/scripts/run_tests
```

## Complete Workflow

To run tests from a clean state:

```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

## Test Coverage

The test suite covers the following modules:
- raft (Raft consensus algorithm)
- pkg/adt (Abstract data types)
- pkg/fileutil (File utilities)
- pkg/idutil (ID utilities)
- pkg/netutil (Network utilities)
- pkg/transport (Transport layer)
- pkg/wait (Wait primitives)
- pkg/pbutil (Protocol buffer utilities)
- pkg/types (Common types)

Total: ~404 unit tests

## Requirements

- Go 1.15+ (tested with Go 1.23.4)
- Standard Unix utilities (grep, wc, etc.)
- Internet connection for downloading dependencies

## Notes

- Scripts are portable and work on both HEAD and HEAD~1 without modification
- All changes are made to git-ignored directories only
- `git status` shows clean working tree after execution
