# Summary

This document describes the testing setup for the Cilium project - a Go-based networking and security solution for cloud-native environments.

## System Dependencies

The Cilium project requires:

- **Go**: Version 1.19 or compatible (the project specifies Go 1.19.2 in GO_VERSION, though it works with newer versions like 1.23.4)
- **Build tools**: Standard Go toolchain with module support
- **Optional (not available in this environment)**: Docker/Podman for running kvstore containers (etcd, consul) during integration tests

Since Docker/Podman are not available in the test environment, the scripts are configured to skip kvstore-dependent tests using `SKIP_KVSTORES="true"`.

## Project Environment

The project uses:

- **Language**: Go 1.19+
- **Build system**: Make-based build system (see Makefile)
- **Dependency management**: Go modules with vendored dependencies
- **Module path**: `github.com/cilium/cilium`

### Environment Variables Set

The setup scripts configure the following environment variables:

- `GO111MODULE=on` - Enable Go modules
- `GOFLAGS="-mod=vendor"` - Use vendored dependencies
- `SKIP_KVSTORES="true"` - Skip kvstore container requirements
- `SKIP_K8S_CODE_GEN_CHECK="true"` - Skip Kubernetes code generation checks
- `CONTAINER_ENGINE=docker` - Set container engine (even though not available)
- `PATH` includes `/testbed/bpf` - For BPF-related test utilities

## Testing Framework

The project uses the standard **Go testing framework** (`go test`).

### Test Organization

- Tests are located throughout the codebase, primarily in the `pkg/` directory
- Test files follow the standard Go convention: `*_test.go`
- There are 369+ test files in the `pkg/` directory alone

### Test Execution

The `run_tests` script executes a representative subset of unit tests focusing on core packages:

- `pkg/alignchecker`, `pkg/allocator`, `pkg/api`, `pkg/checker`, `pkg/cidr`, etc.
- Tests run with a 300-second timeout per package
- Verbose output is captured and parsed to extract test statistics

### Test Output Format

The script outputs a single JSON line with test results:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

Example from a successful run:
```json
{"passed": 130, "failed": 0, "skipped": 1, "total": 131}
```

## Additional Notes

### Limitations

1. **No container runtime**: Docker/Podman are not available, so integration tests requiring kvstores (etcd, consul) are skipped.
2. **Subset of tests**: To keep execution time under 15 minutes, only a representative subset of unit tests from `pkg/` are executed.
3. **Build failures**: Some packages may have build failures (e.g., `pkg/bgp/manager` had a link error related to `golang.org/x/net/internal/socket`), but core functionality tests run successfully.

### Test Suite Coverage

The current test script covers approximately 40+ core packages in the `pkg/` directory, representing the fundamental building blocks of Cilium:
- Core utilities (alignchecker, allocator, api)
- Network primitives (cidr, ipcache, ipam, mac, tuple)
- Identity and policy management (identity, labels, policy)
- Kubernetes integration (k8s packages)
- Service and proxy functionality
- Monitoring and metrics

### Reproducibility

The scripts are designed to work on both HEAD and HEAD~1 commits without modification, ensuring stability across git history changes.
