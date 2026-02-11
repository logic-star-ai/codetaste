# Summary

This repository contains **gqlgen**, a Go library for building GraphQL servers. The testing setup has been configured to run the comprehensive test suite and output results in JSON format.

## System Dependencies

- **Go**: Version 1.23.4 (specified in go.mod: go 1.20 minimum)
- **No additional system services required**: The test suite runs without external dependencies like databases or Redis

## Project Environment

- **Language**: Go
- **Module**: github.com/99designs/gqlgen
- **Package Manager**: Go modules (go mod)
- **Build System**: Native Go toolchain
- **Test Framework**: Go's built-in testing framework with `testing` package and `github.com/stretchr/testify` for assertions

### Key Dependencies
- GraphQL parser: `github.com/vektah/gqlparser/v2`
- Code generation tools: `golang.org/x/tools`
- Testing utilities: `github.com/stretchr/testify`
- Various GraphQL-related libraries (WebSocket support, UUID generation, etc.)

### Environment Variables
- `GO111MODULE=on`: Ensures Go module mode is enabled
- `CGO_ENABLED=1`: Enables CGO for tests that may require it

## Testing Framework

The test suite uses Go's native testing framework (`go test`) with the following characteristics:

- **Test Discovery**: Automatically discovers all `*_test.go` files
- **Test Execution**: Runs approximately 932 tests across 58 packages
- **Test Types**:
  - Unit tests for core GraphQL functionality
  - Code generation tests that verify the gqlgen code generator
  - Integration tests for GraphQL server functionality
  - Parser and validation tests

### Test Results Format

The `/scripts/run_tests` script outputs results in JSON format:
```json
{"passed": 931, "failed": 1, "skipped": 0, "total": 932}
```

### Test Execution

Tests are run using `go test -json ./...` which:
- Executes all tests in the repository (excluding `_examples` directory)
- Outputs structured JSON for each test event
- Parses the JSON output to count passed, failed, and skipped tests

## Additional Notes

### Known Issues
1. **Flaky Test**: One test consistently fails: `TestApolloSandboxHandler_Integrity` in the `graphql/playground` package. This test validates the integrity hash of externally fetched resources and fails due to version mismatches of external dependencies. This is a known issue and not related to the core functionality of gqlgen.

### Generated Files
The test suite includes code generation tests in `plugin/resolvergen/` that regenerate test fixtures during execution. These tests verify that the code generator produces valid Go code. The generated files are committed to the repository and may be modified during test runs, which is expected behavior for validation tests.

### Performance
- Full test suite execution (including setup): ~30-40 seconds
- Most tests complete quickly, with code generation tests taking slightly longer
- Tests run without race detection by default for performance (CI uses `-race` flag)

### Compatibility
The scripts are designed to work on both the current commit (HEAD) and previous commits (HEAD~1), making them suitable for regression testing and bisecting.
