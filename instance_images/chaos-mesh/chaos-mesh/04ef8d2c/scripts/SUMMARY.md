# Summary

This repository contains **Chaos Mesh**, a cloud-native Chaos Engineering platform written in Go. The testing setup focuses on running Go unit tests for the main codebase modules without requiring Kubernetes or Docker infrastructure.

## System Dependencies

The testing environment requires:
- **Go 1.22.5+** (pre-installed: Go 1.23.4)
- **GCC/cc compiler** (for building C test utilities)
- **Standard build tools** (build-essential)

No additional system services (databases, Redis, etc.) are required for the unit tests. The tests run in isolation using Go's testing framework and mock objects.

## Project Environment

The project is a multi-module Go workspace with the following structure:

### Main Module (`/testbed`)
- **go.mod**: go 1.22.5
- Contains the core Chaos Mesh components (controller, daemon, dashboard)
- Dependencies: Kubernetes libraries (k8s.io), gRPC, Gin web framework, and cloud provider SDKs

### API Module (`/testbed/api`)
- **go.mod**: go 1.22
- Contains CRD (Custom Resource Definition) types and webhooks
- Separate module for API versioning and reusability

### E2E Test Module (`/testbed/e2e-test`)
- Contains end-to-end tests (not run in unit test suite)
- Requires Kubernetes cluster

### Test Utilities
The setup builds several C-based test utilities:
- `bin/test/timer`: Timer test utility
- `bin/test/multithread_tracee`: Multi-threaded trace test utility
- `pkg/time/fakeclock/fake_clock_gettime.o`: Fake clock object for time testing
- `pkg/time/fakeclock/fake_gettimeofday.o`: Fake time-of-day object

## Testing Framework

The project uses **Go's native testing framework** with:
- Test files: `*_test.go` (115 test files found)
- Test execution: `go test` with CGO enabled
- Testing libraries: Standard `testing` package, plus Ginkgo/Gomega for some tests

### Test Execution Strategy

The `/scripts/run_tests` script executes a representative subset of tests:
1. **API Module Tests** (`/testbed/api/...`)
2. **Core Package Tests**:
   - `./pkg/webhook/...` - Webhook validation
   - `./pkg/workflow/...` - Workflow controllers
   - `./pkg/selector/...` - Pod/resource selectors
   - `./pkg/dashboard/...` - Dashboard API
   - `./controllers/...` - Kubernetes controllers
   - `./cmd/chaos-builder/...` - Code generation tools

### Test Results Format

The script outputs JSON in the format:
```json
{"passed": 154, "failed": 7, "skipped": 0, "total": 161}
```

**Note**: Some tests fail due to missing Kubernetes environment, but this is expected for unit tests running without a cluster.

## Additional Notes

### Environment Variables
- `CGO_ENABLED=1`: Required for C-based test utilities
- `USE_EXISTING_CLUSTER=false`: Tests run without Kubernetes
- `GO111MODULE=on`: Module-aware mode

### Excluded from Tests
The following are excluded from the test suite:
- `chaos-mesh/test`: Integration tests
- `pkg/ptrace`: Platform-specific tracing
- `vendor`: Third-party dependencies
- `zz_generated`: Auto-generated code

### Portability
All scripts are designed to work on both HEAD and HEAD~1 commits without modification. The scripts:
1. Clean the repository state (`git clean -xdff`)
2. Download dependencies fresh for each run
3. Build required test utilities
4. Execute tests with consistent output format

### Performance
The test suite completes in approximately 1-2 minutes, making it suitable for CI/CD pipelines.
