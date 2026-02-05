# Summary

This testing setup is configured for the Juju project, a Go-based application orchestration engine. The tests use the gocheck testing framework (gopkg.in/check.v1) and require CGO compilation with dqlite support.

## System Dependencies

- **musl-tools**: Required for musl-gcc compiler used for static linking
- **libsqlite3-dev**: Development headers for SQLite3

## Project Environment

- **Language**: Go 1.24.1
- **Build System**: Go modules with CGO enabled
- **Dependencies**:
  - dqlite (distributed SQL database)
  - musl (for static compilation)
  - Various Go dependencies managed via go.mod

### Environment Variables Set by setup_shell.sh:
- `CGO_ENABLED=1`: Enable CGO compilation
- `CC=musl-gcc`: Use musl compiler
- `CGO_CFLAGS`: Include paths for dqlite headers
- `CGO_LDFLAGS`: Link flags for dqlite, sqlite3, and related libraries
- `TEST_BUILD_TAGS=libsqlite3,dqlite`: Build tags for tests
- `PATH`: Updated to include musl binaries

## Testing Framework

The project uses **gocheck** (gopkg.in/check.v1) testing framework, which provides:
- Suite-based test organization
- Rich assertion methods
- Test fixtures and setup/teardown

Test results are identified by lines starting with:
- `OK: X passed` - Successful test suite
- `FAIL: X passed, Y failed` - Failed test suite
- `ok github.com/juju/juju/...` - Successful package

## Scripts

### /scripts/setup_system.sh
No system services required. This is a placeholder that exits successfully.

### /scripts/setup_shell.sh
Must be **sourced** (not executed) to set up the environment:
```bash
source /scripts/setup_shell.sh
```

This script:
1. Verifies Go version matches go.mod requirement
2. Installs musl and dqlite dependencies into `_deps/` directory
3. Downloads Go module dependencies
4. Sets up CGO environment variables for dqlite compilation

### /scripts/run_tests
Runs a representative subset of tests (10 core API packages).

**IMPORTANT**: This script must be run AFTER sourcing setup_shell.sh:
```bash
source /scripts/setup_shell.sh && /scripts/run_tests
```

The script:
1. Verifies environment is set up (checks CGO_ENABLED)
2. Selects core test packages from the api/ directory
3. Runs tests with appropriate build tags
4. Parses gocheck output to count passed/failed tests
5. Outputs JSON with test results

## Invocation Pattern

Complete test run:
```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

Or in a single command:
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Additional Notes

### Challenges Encountered:

1. **CGO Compilation Requirements**: The project requires specific CGO flags for dqlite support. These must be properly configured before running tests.

2. **Environment Persistence**: The setup_shell.sh script MUST be sourced (not executed) to ensure environment variables persist in the current shell. Subprocesses inherit exported variables, but piping or complex bash -c invocations can cause environment loss.

3. **Dqlite Dependencies**: The project uses dqlite which requires musl-gcc and specific library paths. The build system downloads pre-compiled dqlite dependencies into `_deps/` directory.

4. **Test Selection**: Due to the large codebase (500+ packages), the test script runs a representative subset of 10 core API packages to complete within reasonable time (~5 minutes).

5. **Build Tags**: Tests must be run with `-tags="libsqlite3,dqlite"` to enable dqlite support.

### Working Directory

All scripts assume `/testbed/` as the project root. The `_deps/` directory (created for musl/dqlite) is gitignored and will be recreated on each setup.

### Test Output Format

The final line of `/scripts/run_tests` stdout is JSON:
```json
{"passed": X, "failed": Y, "skipped": Z, "total": W}
```

Where values represent counts of individual test cases (not packages).
