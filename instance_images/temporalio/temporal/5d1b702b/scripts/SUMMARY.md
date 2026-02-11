# Summary

This repository contains the Temporal server, a durable execution platform written in Go. The testing environment has been configured to run a representative subset of unit tests that validate the core functionality of the server.

## System Dependencies

No special system-level dependencies are required for running the unit tests. The tests run with:
- **Go 1.23.4** (pre-installed, matches requirement of go 1.23.2+ from go.mod)
- **jq** (for JSON parsing of test results, pre-installed)
- Standard Ubuntu 24.04 build tools

The `/scripts/setup_system.sh` script is a placeholder that exits successfully since no system services (databases, Redis, etc.) are required for the unit test suite.

## Project Environment

The project uses:
- **Language**: Go 1.23.2+ (running with Go 1.23.4)
- **Package Manager**: Go modules (go.mod/go.sum)
- **Build System**: Makefile with extensive targets for building, testing, and linting

### Environment Setup (`/scripts/setup_shell.sh`)

The setup script configures:
1. **Go Environment Variables**:
   - `CGO_ENABLED=0` - Disables CGO for faster builds
   - `GOOS=linux`, `GOARCH=amd64` - Target platform
   - `GOPATH` - Set to system Go path
   - `PATH` - Includes local `.bin` directory for tools

2. **Temporal-specific Variables**:
   - `TEMPORAL_VERSION_CHECK_DISABLED=1` - Disables version checking during tests

3. **Dependencies**:
   - Downloads Go module dependencies via `go mod download`
   - Validates build by compiling the main server binary

The script is idempotent and uses Go's built-in caching to avoid redundant work.

## Testing Framework

The project uses **Go's built-in testing framework** with the following structure:

### Test Organization
The codebase has three main types of tests (per Makefile):
1. **Unit Tests**: Fast tests in most packages (excluding integration/functional directories)
2. **Integration Tests**: Tests in `./common/persistence/tests`, `./tools/tests`, `./temporaltest`, `./internal/temporalite`
3. **Functional Tests**: Tests in `./tests`, `./tests/xdc`, `./tests/ndc` directories

### Test Execution (`/scripts/run_tests`)

The test runner executes a **representative subset of unit tests** covering:
- Core common packages: cache, clock, cluster, collection, convert, dynamicconfig, headers, log, membership, metrics, namespace, primitives, quotas, rpc, searchattribute, util
- Service configuration packages: history configs/queues, matching configs
- Client package
- Temporal and temporaltest packages

**Test Configuration**:
- Timeout: 12 minutes (with 15-minute total allowance)
- Race detector: Disabled for speed
- Test caching: Disabled (`-count=1`)
- Output format: JSON for machine-readable parsing
- Build tags: `,test_dep,` (empty main tag + test dependencies)

**Result Counting**:
The script counts only top-level tests (not subtests) by:
1. Running tests with `-json` flag
2. Parsing JSON output with `jq` to identify pass/fail/skip actions
3. Filtering for test names starting with "Test" and excluding subtests (those containing "/")
4. Counting unique Package::TestName combinations
5. Outputting final JSON: `{"passed": N, "failed": N, "skipped": N, "total": N}`

### Test Results

On both HEAD and HEAD~1:
- **187 tests passed**
- **0 tests failed**
- **0 tests skipped**
- **Total: 187 tests**

Tests complete in approximately 27-30 seconds on the selected subset.

## Additional Notes

### Portability
All three scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. The scripts rely only on:
- The presence of `go.mod` and Go source files
- Standard Go tooling
- The Makefile structure (not directly used, but informed the test selection)

### Performance Considerations
- The full test suite (unit + integration + functional) would take 20-25 minutes per the Makefile
- The selected subset runs in ~30 seconds, providing good coverage while staying well under the 15-minute limit
- Race detection is disabled to prioritize execution speed over concurrency bug detection
- CGO is disabled for faster compilation

### Test Selection Rationale
The test packages were selected to provide:
1. **Broad coverage** across multiple subsystems (common utilities, service configs, client)
2. **Fast execution** (unit tests only, no database/network dependencies)
3. **Stability** across commits (avoiding tests that depend on recent features)
4. **Representative results** of code quality and functionality

### Limitations
- Integration tests requiring databases (Cassandra, MySQL, PostgreSQL, SQLite) are not run
- Functional tests requiring full server setup are not run
- Tests that use the `-race` flag for concurrency bug detection are not enabled
- The test coverage is partial but representative of core functionality
