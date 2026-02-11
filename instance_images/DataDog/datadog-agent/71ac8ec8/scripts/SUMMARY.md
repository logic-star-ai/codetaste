# Summary

This repository contains the Datadog Agent, a polyglot project primarily written in Go with Python tooling for build orchestration. The testing setup is configured to run a representative subset of unit tests from the Go codebase.

## System Dependencies

The project requires:
- **Go 1.22.8** (as specified in `.go-version`, though 1.23.4 works with minor compatibility warnings)
- **Python 3.11** (as specified in `.python-version`)
- **Build tools**: CGO support for building certain packages
- **No system services**: Unit tests run without requiring external services like databases or message queues

System-level dependencies are handled by the pre-installed Ubuntu 24.04 environment:
- GCC/build-essential for CGO compilation
- Standard system libraries (SSL, pthread, etc.)

## Project Environment

### Python Environment
The project uses Python's `invoke` task runner for build orchestration. A virtual environment is created at `/testbed/venv` with the following dependencies:
- `invoke` - Task execution framework
- `requests`, `pyyaml`, `colorama`, `GitPython` - Core utilities
- `python-gitlab`, `dulwich`, `semver`, `docker` - Build/CI integration tools

### Go Environment
- **Module**: `github.com/DataDog/datadog-agent`
- **Build mode**: Go modules with vendoring support
- **CGO**: Enabled (`CGO_ENABLED=1`) for native integrations
- **Build flags**: `-buildvcs=false` to disable VCS stamping in tests

Environment variables:
- `GOPATH`: `$HOME/go`
- `PROJECT_ROOT`: `/testbed`
- Go bin and GOPATH/bin added to PATH

### Dependency Management
- Go dependencies are cached by Go's module system after initial download
- Python dependencies are installed once in the virtual environment
- Both are idempotent - re-running setup scripts doesn't reinstall if already present

## Testing Framework

### Test Execution
The project uses Go's native testing framework (`go test`). Tests are executed with:
- `-short` flag to skip long-running integration tests
- `-v` flag for verbose output to enable accurate result parsing
- `10m` timeout to prevent hanging tests
- Targets first 100 packages with test files from `./pkg/...`

### Test Selection
The test runner automatically discovers test packages using:
```bash
go list -f '{{if .TestGoFiles}}{{.ImportPath}}{{end}}' ./pkg/...
```

This ensures only packages with actual test files are included, avoiding build failures on packages without tests.

### Result Parsing
Test results are parsed from Go's verbose output by counting:
- `--- PASS: TestName` - Individual passing tests
- `--- FAIL: TestName` - Individual failing tests
- `--- SKIP: TestName` - Skipped tests
- `ok package_name` / `FAIL package_name` - Package-level results as fallback

Results are output in JSON format:
```json
{"passed": 363, "failed": 2, "skipped": 2, "total": 367}
```

### Test Results
On current HEAD (fdca9fe), the test suite reports:
- **363 passing tests** across multiple packages
- **2 failing tests** (in compliance and config/legacy packages - environment detection issues)
- **2 skipped tests**
- **Total: 367 tests** executed in ~8-10 minutes

The same results are observed on HEAD~1 (71ac8ec), confirming script portability.

## Additional Notes

### Known Issues
1. **Go version mismatch**: The environment has Go 1.23.4, but the project specifies 1.22.8. Tests run successfully with only warnings about the version difference.

2. **Some test failures**: Two packages have failing tests related to cloud provider environment detection:
   - `pkg/compliance`: Tests fail when trying to detect AWS/cloud environments
   - `pkg/config/legacy`: Kubernetes configuration tests panic due to environment detection

   These failures appear to be environmental (missing cloud metadata endpoints) rather than actual code issues.

3. **Build constraints**: Some packages (e.g., `pkg/aggregator`) have build failures in benchmark tests due to missing test dependencies. The `-short` flag helps avoid these, but some build errors still occur.

### Performance
- Test execution completes within 10 minutes (well under the 15-minute target)
- Go's test cache significantly speeds up repeated runs
- Python environment setup adds ~10 seconds on first run, cached thereafter

### Portability
The scripts are designed to work across commits:
- No hardcoded paths or commit-specific logic
- Version detection from `.go-version` and `.python-version` files
- Idempotent setup allows re-running without side effects
- Works on both HEAD and HEAD~1 without modifications
