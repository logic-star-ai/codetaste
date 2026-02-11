# Summary

This repository is **Bytebase**, a Database CI/CD solution built with Go and featuring a full-stack architecture (Go backend + Vue.js frontend). The testing setup has been configured to run backend unit tests focusing on common utility packages.

## System Dependencies

No system-level dependencies are required for running the tests. The test suite uses:
- **Go 1.23.4** (compatible with required Go 1.21.5)
- Embedded PostgreSQL and MySQL instances (downloaded automatically during setup)

The embedded database binaries are managed via `go generate` commands that download MySQL 8.0.33 for the appropriate platform.

## Project Environment

### Language & Runtime
- **Primary Language**: Go (backend)
- **Go Version**: 1.21.5 specified in go.mod, but compatible with Go 1.23.4
- **Build Tags**: `mysql` tag required for embedding MySQL test resources

### Key Environment Variables
- `GOPRIVATE="github.com/bytebase/*"`: Skip checksum verification for Bytebase private modules
- `GONOSUMDB="github.com/bytebase/*"`: Skip sum database for Bytebase modules
- `GOPROXY="https://proxy.golang.org,direct"`: Use standard Go proxy
- `CGO_ENABLED=1`: Required for some database drivers

### Dependencies
The project has extensive dependencies including:
- Database drivers (MySQL, PostgreSQL, MongoDB, Snowflake, etc.)
- gRPC and Protocol Buffers
- Various cloud SDKs (AWS, Azure, Google Cloud)
- Custom Bytebase parsers (MySQL, PostgreSQL, TiDB, TSQL, etc.)

## Testing Framework

### Framework
- **Testing Tool**: Go's built-in `testing` package
- **Assertion Library**: `github.com/stretchr/testify`
- **Mock Framework**: `github.com/google/go-cmp` for comparisons

### Test Execution
Tests are run using standard `go test` commands with the following parameters:
- `-tags mysql`: Enable MySQL-specific build tags
- `-v`: Verbose output for result parsing
- `-timeout 15m`: 15-minute timeout
- `-p 4`: Run up to 4 test packages in parallel

### Test Scope
Due to dependency issues with private Bytebase parser modules (`tidb-parser`, `tsql-parser`), the test execution is limited to:
- `./backend/common/...`: Common utility functions (11 tests)
- `./backend/common/stacktrace`: Stack trace utilities

These packages are self-contained and don't require database connectivity or the problematic parser dependencies.

### Test Count
- **Total Tests**: 11
- **Test Categories**:
  - String manipulation and truncation
  - External URL normalization
  - Phone number validation
  - Obfuscation utilities
  - Stack trace generation

## Additional Notes

### Obstacles Encountered

1. **Private Module Dependencies**: The repository depends on several private Bytebase forks of open-source projects:
   - `github.com/bytebase/tidb-parser`
   - `github.com/bytebase/tsql-parser`

   These modules use pseudo-versions pointing to specific commits that are not publicly accessible, causing download failures. This limits the scope of tests that can be run in this environment.

2. **Workaround**: The test suite focuses on the `backend/common` package which contains utility functions and doesn't depend on database-specific parsers. This still provides meaningful test coverage of core utility functions.

3. **Full Test Suite**: In a production CI/CD environment with proper access to private repositories, the full test suite would include:
   - `backend/api/...`: API layer tests
   - `backend/plugin/advisor/...`: SQL advisor rules
   - `backend/tests/...`: Integration tests with embedded databases
   - Additional plugin and database-specific tests

4. **MySQL Resources**: The `go generate` step successfully downloads MySQL 8.0.33 binaries (~57MB) which are used by integration tests (though not executed in this limited scope).

### Script Portability

All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. They handle the repository state gracefully and don't modify version-controlled files.
