# Summary

This testing setup configures the Cosmos SDK repository for running a representative subset of tests. The Cosmos SDK is a Go-based blockchain application framework that uses a multi-module architecture with workspace management.

## System Dependencies

No external system dependencies or services are required for running the test suite. The tests run entirely in-memory without requiring:
- Database services (PostgreSQL, MySQL, etc.)
- Message queues (Redis, RabbitMQ, etc.)
- External APIs or services

The only requirements are:
- Go 1.19+ (pre-installed as Go 1.23.4 in the environment)
- Standard build tools (gcc, make) for CGO-enabled tests
- The `jq` utility for JSON parsing in test result aggregation

## Project Environment

### Language and Runtime
- **Primary Language**: Go
- **Required Version**: Go 1.19+ (as specified in go.mod)
- **Installed Version**: Go 1.23.4

### Module Structure
The Cosmos SDK uses a multi-module architecture with the following key modules:
- **Main module** (`github.com/cosmos/cosmos-sdk`): Core SDK functionality
- **Sub-modules**: `api`, `tests`, `collections`, `errors`, `core`, `simapp`, `math`, `orm`, `depinject`, `tx`, `client/v2`, and various tools

Each module has its own `go.mod` file and dependency tree.

### Dependency Management
Dependencies are managed using Go modules (`go.mod` and `go.sum`). The setup script:
1. Downloads dependencies for the main module
2. Iterates through all sub-modules and downloads their dependencies
3. Optionally installs `tparse` for enhanced test output parsing

### Build Tags
Tests are run with the following build tags:
- `cgo`: Enable CGO support
- `ledger`: Enable Ledger hardware wallet support (mocked)
- `test_ledger_mock`: Use mock Ledger implementation for testing
- `norace`: Disable race detection for faster execution

## Testing Framework

### Test Framework
The project uses Go's native testing framework (`testing` package) with additional libraries:
- `github.com/stretchr/testify`: Assertion and mocking utilities
- `pgregory.net/rapid`: Property-based testing

### Test Execution Strategy
The `/scripts/run_tests` script executes a representative subset of tests across multiple modules:

**Main Module Packages** (tested sequentially):
- `./version`: Version information and commands
- `./codec`: Encoding/decoding functionality
- `./crypto/keys/ed25519`: Ed25519 cryptographic keys
- `./crypto/keys/secp256k1`: Secp256k1 cryptographic keys
- `./types/address`: Address handling and validation

**Sub-modules** (tested in their respective directories):
- `math`: Mathematical operations and utilities
- `errors`: Error handling and types
- `collections`: Collection data structures

### Test Execution
Tests are run with:
- JSON output format for machine-parseable results
- 2-minute timeout per package
- Read-only mode (`-mod=readonly`) to ensure dependency integrity

### Result Aggregation
The test script:
1. Runs each package/module separately
2. Captures JSON output from `go test`
3. Parses JSON using `jq` to extract test results
4. Counts passed, failed, and skipped tests
5. Outputs a single JSON line: `{"passed": N, "failed": N, "skipped": N, "total": N}`

### Test Coverage
The representative subset includes approximately **328 tests** covering:
- Version management
- Codec operations
- Cryptographic key operations (Ed25519, Secp256k1)
- Address handling
- Mathematical operations
- Error handling
- Collection data structures

This subset provides good coverage of core functionality while completing in under 5 minutes.

## Additional Notes

### Portability
All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification. This ensures the testing infrastructure remains stable across commits.

### Clean Repository State
The scripts are designed to:
- Only modify files that are ignored by version control (e.g., build artifacts, `vendor/`, dependency caches)
- Ensure `git status` shows no changes after setup
- Support clean testing via `git clean -xdff` followed by setup

### Performance Considerations
- Total execution time: ~2-3 minutes on a modern system
- Sequential package testing prevents resource contention
- Dependency downloads are cached by Go's module cache
- The setup script is idempotent and skips redundant installations

### Potential Extensions
For more comprehensive testing, additional packages can be added to the `MAIN_PACKAGES` array in `/scripts/run_tests`, such as:
- `./baseapp`: Base application framework
- `./store/*`: Storage layer implementations
- `./client/*`: Client libraries
- Integration and E2E tests from the `./tests` module

However, these would significantly increase execution time beyond the 15-minute target.
