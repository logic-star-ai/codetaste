# Summary

This repository contains **KubeVirt**, a virtual machine management add-on for Kubernetes. The testing setup has been configured to run a comprehensive subset of unit tests using Go's native test runner with the Ginkgo v2 testing framework.

## System Dependencies

**No system-level dependencies or services are required** for running the unit tests. The tests are self-contained and do not require:
- Running databases (PostgreSQL, MySQL, Redis, etc.)
- System daemons or services
- Container runtimes (Docker, Podman)
- Kubernetes clusters

All system dependencies are handled by the pre-existing vendor directory in the repository.

## Project Environment

- **Language**: Go 1.19+ (tested with Go 1.23.4)
- **Package Manager**: Go modules with vendoring (`go mod vendor`)
- **Build System**: Bazel (optional, not used for unit tests)
- **Go Environment Variables**:
  - `GOFLAGS="-mod=vendor"` - Uses vendored dependencies
  - `GO111MODULE=on` - Enables Go modules
  - `KUBEVIRT_NO_BAZEL=true` - Disables Bazel for unit tests
  - `KUBEVIRT_DIR=/testbed` - Repository root directory

The project uses a vendored dependency approach, meaning all third-party dependencies are included in the repository under the `vendor/` directory. This ensures reproducible builds and eliminates the need for network access during testing.

## Testing Framework

The project uses **Ginkgo v2** (github.com/onsi/ginkgo/v2) as the BDD-style testing framework, along with **Gomega** for assertions. Tests are executed using Go's standard `go test` command.

### Test Structure

- Unit tests are located throughout the codebase in `*_test.go` files
- Each package typically has a `*_suite_test.go` file that sets up the Ginkgo test suite
- Test packages cover various components:
  - **Core**: instancetype, container-disk, emptydisk, executor, config
  - **Storage**: types, snapshot, export functionality
  - **Operator**: resource generation, RBAC, component management
  - **Network**: cache, naming schemes, link management, VMI specifications
  - **virt-launcher**: virtwrap API, converter, device management
  - **Client libraries**: kubecli, logging from staging/src/kubevirt.io/client-go

### Test Execution

The test script runs approximately **33 test packages** covering over **1000 individual test specifications**. Tests complete in approximately **5 minutes** on the provided environment.

Test output format:
```json
{"passed": 1065, "failed": 0, "skipped": 0, "total": 1065}
```

### Running Tests

```bash
# Full workflow
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

## Additional Notes

### Vendor Directory
The repository includes a comprehensive vendor directory (~200MB) containing all Go dependencies. This means:
- No external network access is required for dependencies
- Tests run in an isolated, reproducible environment
- The setup is compatible with air-gapped environments

### Test Coverage
The selected test packages provide representative coverage across:
- Core KubeVirt functionality (VM management, configuration)
- Storage and disk management
- Operator and lifecycle management
- Network configuration and management
- API client libraries
- Low-level virtualization wrapper components

### Performance
- Individual package tests typically complete in under 1 second
- Total test suite completes in ~5 minutes
- Tests use Go's race detector (`-race` flag in Bazel builds, but not in go test for speed)
- Tests are parallelizable and run efficiently on multi-core systems

### Compatibility
The scripts are designed to work across Git commits and are portable:
- Successfully tested on both HEAD and HEAD~1
- Do not modify version-controlled files
- All modifications are in `_out/` directory (gitignored)
- Environment setup is idempotent and can be run multiple times safely
