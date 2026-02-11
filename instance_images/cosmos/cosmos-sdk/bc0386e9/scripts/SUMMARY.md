# Summary

This testing setup is configured for the Cosmos SDK, a blockchain application framework written in Go. The scripts enable automated testing across different commits while maintaining environment consistency.

## System Dependencies

No system-level dependencies are required for running the Cosmos SDK tests. The project uses pure Go dependencies that are managed through Go modules.

**System Setup Script:** `/scripts/setup_system.sh`
- No system services need to be started
- Script exits successfully with no operations

## Project Environment

**Language:** Go 1.19+ (tested with Go 1.23.4)
**Package Manager:** Go modules (`go mod`)

**Shell Setup Script:** `/scripts/setup_shell.sh`
- Sets up Go environment variables (`GOPATH`, `PATH`)
- Enables CGO for optional C dependencies
- Downloads and verifies Go module dependencies
- Optionally installs `tparse` for better test output formatting

**Key Environment Variables:**
- `CGO_ENABLED=1` - Enables CGO support for certain database backends
- `GOPATH` - Set to `$HOME/go`

## Testing Framework

**Framework:** Go's built-in testing framework (`go test`)

**Test Runner Script:** `/scripts/run_tests`
- Runs a representative subset of tests (completes within 15 minutes)
- Uses build tags: `norace ledger test_ledger_mock`
- Tests core packages: types, codec, store/types, auth/types, bank/types
- Tests integration packages: bank/keeper, distribution/keeper
- Outputs results in JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

**Test Coverage:**
- Unit tests for core SDK components
- Integration tests for key modules (bank, distribution)
- Approximately 630-640 tests run per execution

**Test Output:**
- JSON format with structured test events
- Final line contains summary statistics
- Diagnostic messages written to stderr, results to stdout

## Additional Notes

**Portability:**
- Scripts are designed to work on both current commit (HEAD) and previous commit (HEAD~1)
- No modifications to versioned files in `/testbed/`
- All dependencies are installed via Go modules, preserving git cleanliness

**Performance:**
- Test suite completes in approximately 5-10 minutes
- Selected test packages provide good coverage of core functionality
- Timeout set to 10 minutes per package to handle slower tests

**Build Tags:**
- `norace` - Disables race detector for faster execution
- `ledger` - Enables ledger hardware wallet support
- `test_ledger_mock` - Uses mock ledger for testing without hardware

**Determinism:**
- Test results are deterministic and reflect actual test outcomes
- Test counts may vary slightly between commits as tests are added/removed
- JSON parser correctly counts only test-level results (not package-level results)
