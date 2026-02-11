# Summary

This repository contains **Tekton Pipelines**, a Kubernetes-native CI/CD framework written in **Go**. The test setup focuses on running unit tests for the core packages while excluding end-to-end and conformance tests that require a Kubernetes cluster.

## System Dependencies

- **Go 1.23.4** (pre-installed, meets requirement of Go 1.19+ from go.mod)
- **Python 3** (for JSON parsing in test result aggregation)
- No additional system services or packages required

## PROJECT Environment

### Language & Version
- **Language**: Go
- **Required Version**: 1.19+ (specified in go.mod)
- **Actual Version**: 1.23.4

### Dependencies
- All dependencies are managed via **Go modules** with vendoring
- The `vendor/` directory is committed to the repository
- Tests use `-mod=vendor` flag to ensure deterministic builds
- No additional installation required as vendor directory is complete

### Environment Variables
- `GO111MODULE=on` - enables Go modules
- `CGO_ENABLED=1` - enables CGO support (required by some dependencies)

## Testing Framework

### Framework
**Go's built-in testing framework** (`go test`)

### Test Structure
- **Unit tests**: Located alongside source code in `./pkg/...`, `./cmd/...`, and `./internal/...`
- **E2E tests**: Located in `./test/` directory (excluded from our test run as they require Kubernetes)
- **Test tags**: E2E tests use `// +build e2e` build constraint to separate them from unit tests

### Test Execution
- Command: `go test -json -timeout=14m -mod=vendor ./pkg/... ./cmd/... ./internal/...`
- Format: JSON output for easy parsing
- Timeout: 14 minutes (with 1-minute buffer within the 15-minute limit)
- Coverage: 880 unit tests across core packages
- Duration: ~18 seconds on current hardware

### Result Parsing
- Custom Python script (`/scripts/parse_test_results.py`) parses JSON output
- Counts only top-level tests (excludes subtests to avoid double-counting)
- Outputs: `{"passed": N, "failed": N, "skipped": N, "total": N}`

### Test Results (HEAD)
- **Passed**: 879 tests
- **Failed**: 0 tests
- **Skipped**: 1 test
- **Total**: 880 tests

## Additional Notes

### Portability
All scripts are designed to work on both HEAD and HEAD~1 without modifications, as they:
- Use standard Go tooling commands
- Rely on committed vendor directory
- Don't require code generation or build artifacts
- Only modify files ignored by git (none required for tests)

### Constraints Satisfied
1. ✅ No modifications to versioned files in `/testbed/`
2. ✅ Scripts work on both HEAD and HEAD~1
3. ✅ Tests complete well within 15-minute limit (~18 seconds)
4. ✅ JSON output in required format
5. ✅ `git status` shows clean working tree after execution

### Excluded Tests
- **E2E tests** (`./test/` with `-tags=e2e`): Require Kubernetes cluster
- **Conformance tests** (`-tags=conformance`): Require Kubernetes cluster
- **YAML tests**: Require Kubernetes cluster and kubectl
- **Windows tests** (`-tags=windows_e2e`): Require Windows nodes

These excluded tests would require significant infrastructure setup (Kubernetes cluster, ko tool, kubectl, etc.) and are not suitable for the 15-minute time constraint.
