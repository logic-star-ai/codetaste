# Summary

This repository contains **etcd**, a distributed reliable key-value store written in **Go**. The testing environment has been configured to run unit tests for core modules of the etcd codebase.

## System Dependencies

- **Go**: Version 1.23.4 (pre-installed, compatible with etcd's requirement of Go 1.15+)
- **gobin**: Tool required by etcd's build system (installed via `go install github.com/myitcv/gobin@v0.0.14`)
- **Build tools**: Standard Go toolchain (go build, go test)
- **No external services required**: Unit tests run standalone without database or service dependencies

## Project Environment

### Language and Build System
- **Primary Language**: Go
- **Module System**: Go modules (go.mod)
- **Build Script**: `./build.sh` - Builds etcd and etcdctl binaries
- **Test Framework**: Go's native testing framework

### Module Structure
The repository is organized into multiple Go modules:
- `raft/` - Raft consensus algorithm implementation (core module)
- `client/v3/` - Client library for etcd v3 API
- `server/` - Server implementation
- `pkg/` - Shared utility packages
- `api/`, `etcdctl/`, `tests/` - Additional modules

### Dependencies Installation
- Dependencies are managed via `go mod download`
- All dependencies are fetched from the Go module proxy
- The build process requires building the main binaries first (etcd and etcdctl)

## Testing Framework

### Test Execution
Tests are executed using Go's built-in test runner with the following configuration:
- **Command**: `go test -json -short -timeout=90s ./...`
- **Output Format**: JSON (using `-json` flag for structured output)
- **Test Mode**: Short mode (`-short`) to skip long-running tests
- **Timeout**: 90 seconds per test package to prevent hangs

### Test Modules Coverage
The test suite covers the following representative modules:
1. **raft** - Core consensus algorithm (181 tests)
2. **pkg/adt** - Abstract data types (8 tests)
3. **pkg/fileutil** - File utilities (49 tests)
4. **pkg/idutil** - ID generation utilities (2 tests)
5. **pkg/netutil** - Network utilities (18 tests)
6. **pkg/transport** - Transport layer (72 tests)
7. **pkg/wait** - Wait/synchronization primitives (8 tests)
8. **pkg/pbutil** - Protocol buffer utilities (12 tests)
9. **pkg/types** - Common types (54 tests)

**Total**: 404 unit tests executed

### Test Results Format
The `/scripts/run_tests` script outputs a single JSON line:
```json
{"passed": 404, "failed": 0, "skipped": 0, "total": 404}
```

This format is parsed from Go's JSON test output by:
1. Collecting all test events with `"Action":"pass"`, `"Action":"fail"`, or `"Action":"skip"`
2. Filtering for test-level events (those with `"Test"` field)
3. Counting occurrences of each action type

## Additional Notes

### Time Constraints
- The selected test modules were chosen to complete within 15 minutes
- Full test suite includes integration, e2e, and functional tests that take significantly longer
- Race detection (`-race` flag) was disabled to improve performance
- Each module has a 120-second timeout to prevent hangs

### Build Requirements
- The build system requires `gobin` tool for dependency management
- The `build.sh` script must be sourced by `test.sh` to set up environment
- Binaries are built into `/testbed/bin/` directory (git-ignored)

### Portability
- Scripts work on both HEAD and HEAD~1 commits without modification
- All changes are made to git-ignored directories only
- `git status` shows clean working tree after test execution

### Known Limitations
- Full test suite (including integration/e2e tests) requires additional setup
- Some tests depend on etcd binaries being built first
- Tests that require multiple etcd instances or external dependencies are not included
