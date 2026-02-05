# Summary

This document describes the testing setup for NSQ, a realtime distributed messaging platform.

## System Dependencies

No system services are required for NSQ tests. The test script starts nsqlookupd and nsqd services as background processes before running tests and cleans them up afterward.

## PROJECT Environment

NSQ is a legacy Go project that uses the GOPATH workflow without go.mod. The setup includes:

- **Go Version**: Go 1.23.4 (compatible with older code using GO111MODULE=off)
- **GOPATH Setup**: Project is symlinked to `$GOPATH/src/github.com/bitly/nsq`
- **Dependencies**: Manually cloned from GitHub to GOPATH using specific commits from the Godeps file

### Dependency Management

The project uses a `Godeps` file to specify dependencies. Since the original `gpm` tool doesn't work well with modern Go, dependencies are manually cloned to the correct GOPATH locations. Key dependencies include:

- **code.google.com/p/snappy-go**: Migrated from Google Code to github.com/golang/snappy. Using v0.0.4 for API compatibility with go-snappystream.
- **github.com/bitly/go-nsq**: Using nsqio/go-nsq repository (the project was moved).
- **github.com/mreiferson/go-snappystream**: Using commit 7757b68 (before API breaking change).

### Special Handling

1. **Snappy Package**: The old `code.google.com/p/snappy-go/snappy` import path requires creating a subdirectory structure and copying source files (excluding test files) to avoid go.mod conflicts.

2. **Import Path Comment**: The snappy package's import comment declaring `github.com/golang/snappy` is removed using sed to avoid module path conflicts.

## Testing Framework

NSQ uses Go's built-in testing framework (`go test`). Tests are located across multiple packages:

- `nsqd/`: Core message queue daemon tests
- `nsqlookupd/`: Service discovery tests
- `internal/pqueue/`: Priority queue tests
- `internal/protocol/`: Protocol implementation tests

### Test Execution

The test runner:
1. Builds and starts nsqlookupd on a random port as a background service
2. Builds and starts nsqd with TLS configuration as a background service
3. Waits 0.5s for services to initialize
4. Runs `go test -timeout 60s -v ./...` to execute all tests
5. Parses test output to count passed/failed/skipped tests
6. Outputs results as JSON: `{"passed": N, "failed": M, "skipped": K, "total": T}`
7. Cleans up background services and temporary files

### Test Results

On both HEAD (e010e1d) and HEAD~1 (d9193b6):
- **Passed**: 74 tests
- **Failed**: 3 tests
- **Skipped**: 0 tests
- **Total**: 77 tests

## Additional Notes

### Challenges Encountered

1. **Legacy Dependency Management**: The project predates go modules and uses a `Godeps` file. Modern `go get` with `GO111MODULE=off` doesn't work reliably, requiring manual git clones.

2. **Package Migration**: Several dependencies moved from their original locations:
   - `code.google.com/p/snappy-go` → `github.com/golang/snappy`
   - `github.com/bitly/go-nsq` → `github.com/nsqio/go-nsq`

3. **API Compatibility**: The `go-snappystream` dependency's version in Godeps (307a466) expects an older snappy API that returns `([]byte, error)` instead of just `[]byte`. Using commit 7757b68 (before the optimization) resolves this.

4. **Import Path Conflicts**: Modern Go packages include import path comments and go.mod files that conflict with the old GOPATH-style imports. These need to be removed or worked around.

### Environment Variables

The following environment variables must be set for tests to run:
- `GOPATH`: Set to `$HOME/go`
- `GO111MODULE`: Set to `off` to use GOPATH mode
- `PATH`: Extended to include `$GOPATH/bin`

All scripts properly export and preserve these variables.
