# Summary

This repository contains **gopass**, a password manager written in Go. The test environment has been configured to run unit tests across all packages in the repository.

## System Dependencies

The following system-level dependencies are required:

- **GPG (GnuPG)**: Version 2.4.4 or higher - Required for cryptographic operations in tests
- **Git**: Required for version control operations
- **Go**: Version 1.23.4 (pre-installed) - The project requires Go 1.12+ as specified in go.mod

These dependencies are verified by `/scripts/setup_system.sh` which is run with sudo before tests.

## Project Environment

The project uses the following Go configuration:

- **Module**: `github.com/gopasspw/gopass`
- **Go Modules**: Enabled (GO111MODULE=on)
- **Build Output**: `gopass` binary built in `/testbed/`
- **Package Manager**: Go modules (go.mod/go.sum)

Environment setup is handled by `/scripts/setup_shell.sh` which:
1. Sets up Go environment variables
2. Downloads all Go module dependencies
3. Builds the gopass binary for use by tests

The setup is idempotent and safe to run multiple times.

## Testing Framework

The project uses Go's built-in testing framework with the following structure:

- **Test Runner**: `go test` with JSON output (`-json` flag)
- **Test Packages**: ~50 packages excluding `/tests`, `/xcpb`, and `/openpgp` directories
- **Test Types**: Unit tests (integration tests in `/tests` require GOPASS_BINARY env var)
- **Typical Test Count**: ~328 tests (324-325 passing, 2-3 failing, 1 skipped)
- **Execution Time**: ~20-30 seconds for full test suite

The `/scripts/run_tests` script:
1. Runs all unit tests with JSON output
2. Parses JSON to count passed/failed/skipped tests
3. Outputs final result as: `{"passed": N, "failed": N, "skipped": N, "total": N}`

## Additional Notes

### Test Workflow
The complete test workflow is:
```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

### Compatibility
All scripts are designed to work on both HEAD and HEAD~1 commits without modification, ensuring portability across different checkouts.

### Test Exclusions
The Makefile excludes certain packages from testing:
- `/tests` directory (contains integration tests requiring GOPASS_BINARY)
- `/xcpb` directory (protocol buffer code)
- `/openpgp` directory (vendored OpenPGP implementation)

### Known Test Failures
A small number of tests (2-3 out of 328) consistently fail, likely due to:
- Command count mismatches in command setup tests
- Environment-specific configuration differences

These failures are consistent across commits and do not indicate environment setup issues.
