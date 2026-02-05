# Summary

This repository contains Knative Serving, a Kubernetes-based serverless platform written in Go. The testing setup has been configured to run unit tests across all non-integration test packages.

## System Dependencies

No system-level dependencies or running services are required for running the unit test suite. All necessary dependencies are vendored in the repository.

## PROJECT Environment

The project uses Go with the traditional GOPATH-based structure (pre-Go modules era):

- **Language**: Go 1.23.4
- **Dependency Management**: `dep` (dependencies are vendored in `/vendor/` directory)
- **Project Structure**: The code expects to be located at `$GOPATH/src/github.com/knative/serving`
- **Environment Variables**:
  - `GOPATH`: Set to `$HOME/go`
  - `GO111MODULE`: Set to `off` to use vendored dependencies
  - `ARTIFACTS`: Directory for test artifacts (default: `/tmp/artifacts`)
  - `PATH`: Extended to include `$GOPATH/bin`

The setup creates a symbolic link from `/testbed` to `$GOPATH/src/github.com/knative/serving` to maintain the expected directory structure while working with the testbed directory.

## Testing Framework

The project uses Go's built-in testing framework (`go test`):

- **Unit Tests**: Located alongside source code in `*_test.go` files
- **Test Execution**: Uses `go test -v -short` to run tests with shortened timeouts
- **Test Coverage**: Tests 177 packages excluding:
  - `/test/e2e` - End-to-end tests (require running Kubernetes cluster)
  - `/test/conformance` - Conformance tests (require running Kubernetes cluster)
  - `/test/performance` - Performance tests (require running Kubernetes cluster)
  - `/test/upgrade` - Upgrade tests (require running Kubernetes cluster)

The test results are parsed from Go's verbose test output and formatted as JSON with the following structure:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Test Results
- On the current commit (a171e82), the test suite runs 572 tests: 570 passing, 2 failing, 0 skipped
- The same results were observed on HEAD~1 (eab30b3), indicating the test environment is stable
- The two failing tests appear to be pre-existing test failures in the codebase:
  - `TestActivationHandler/active_endpoint` - related to HTTP response code handling
  - `TestHTTPScrapeClient_Scrape_ErrorCases/Error_got_when_sending_request` - related to HTTP scraping

### Integration Tests
This setup focuses on unit tests only. The repository contains extensive integration, conformance, and performance tests that require:
- A running Kubernetes cluster
- Istio service mesh
- Various test images deployed
- kubectl and other Kubernetes tooling

These integration tests are excluded from the current test runner to provide a fast, deterministic test suite that can run in any CI/CD environment without external dependencies.

### Portability
The scripts are designed to work across different commits in the repository's history, as long as the basic Go project structure remains consistent. They have been tested on both HEAD and HEAD~1.
