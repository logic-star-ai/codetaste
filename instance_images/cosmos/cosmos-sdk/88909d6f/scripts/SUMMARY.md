# Summary

This repository contains the Cosmos SDK, a framework for building blockchain applications written in Go. The project uses a multi-module Go workspace structure with separate go.mod files for different components.

## System Dependencies

- **Go**: Version 1.19+ required (Go 1.23.4 installed and compatible)
- **Operating System**: Linux (tested on Ubuntu 24.04)
- **Build Tools**: Standard Go toolchain, no additional system packages required
- **System Services**: None required for unit tests

## PROJECT Environment

The Cosmos SDK is structured as a multi-module Go project with the following key characteristics:

### Project Structure
- **Primary Language**: Go (v1.19+)
- **Module Organization**: Main module at root with 22+ sub-modules (e.g., `math/`, `store/`, `api/`, `tests/`, `tools/`, `x/*/`)
- **Package Manager**: Go modules (go mod)
- **Build System**: Makefile with multiple build targets

### Dependencies Installation
All Go dependencies are installed via `go mod download` for both the main module and all sub-modules. The setup script automatically:
1. Downloads main module dependencies
2. Iterates through all sub-modules and downloads their dependencies
3. Installs `tparse` tool for improved test output parsing (optional)

### Test Tags
The project uses build tags for different test configurations:
- `cgo`: Enable cgo tests
- `ledger`: Enable ledger-related tests
- `test_ledger_mock`: Use mock ledger for tests
- `norace`: Disable race detection for faster test execution

## Testing Framework

### Framework
- **Test Framework**: Go's native testing framework (`go test`)
- **Test Execution**: JSON output mode for structured test result parsing
- **Test Organization**: Unit tests, integration tests (in `tests/` subdirectory), and end-to-end tests

### Test Execution Strategy
The full test suite is extensive and takes significant time. For this setup, we run a representative subset focusing on core packages:
- `baseapp` - Base application layer
- `client` - Client functionality
- `codec` - Encoding/decoding
- `crypto/...` - Cryptographic functions
- `types` and `types/...` - Core types
- `x/auth/...` - Authentication module
- `x/bank/...` - Bank module
- `server` - Server functionality

### Test Results
Typical test run produces:
- **Total**: ~2586 tests
- **Passed**: ~2585 tests
- **Failed**: 0 tests
- **Skipped**: ~1 test
- **Duration**: ~2-3 minutes for the representative subset

### JSON Output Format
The test runner outputs results in the required JSON format:
```json
{"passed": 2585, "failed": 0, "skipped": 1, "total": 2586}
```

## Additional Notes

### Compatibility
- Scripts are portable and work on both HEAD and HEAD~1 commits without modification
- The git working tree remains clean - no source files are modified during setup/testing
- All dependencies are downloaded into Go's cache and module directories outside `/testbed`

### Idempotency
- The `setup_shell.sh` script is idempotent and can be run multiple times safely
- Dependency downloads are cached by Go's module system

### Multi-Module Structure
The Cosmos SDK uses Go workspaces with separate go.mod files for:
- Core modules (math, store, core, errors, log, collections, orm, depinject)
- Extension modules (x/nft, x/circuit, x/upgrade, x/evidence, x/tx, x/feegrant)
- Tools (cosmovisor, rosetta, confix, hubl)
- Testing infrastructure (tests/, api/, client/v2/)
- Main application (simapp/)

This structure allows independent versioning and development of different components while maintaining the overall SDK cohesion.
