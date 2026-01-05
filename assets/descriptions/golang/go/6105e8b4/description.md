# Consolidate misc/cgo/test files to reduce compilation overhead

## Summary
Merge multiple small cgo test files into fewer consolidated files to reduce build time. Each file with `import "C"` requires separate cgo compilation/analysis, causing significant overhead.

## Why
- Current structure has many files with individual `import "C"` statements
- Each must be compiled and analyzed separately by cgo
- Test is built 4 times during all.bash (different settings), multiplying the cost
- `go test -c` takes 20+ seconds on typical laptop

## Changes
- Consolidate into two main files:
  - `test.go` - C definitions + tests (no //export directives)
  - `testx.go` - //export directives + Go exports (C declarations only)
- Move C code from 50+ files into consolidated preambles
- Organize by issue number for maintainability
- Merge test functions into consolidated files
- Remove redundant platform-specific stubs
- Add platform-specific variants (test_unix.go, test_windows.go) where needed

## Expected Impact
- `go test -c` drops from 20s to under 5s
- Removes ~23.4r 29.0u 21.5s from all.bash
- No test coverage lost
- Single import "C" per main file = single cgo invocation

## Notes
- Separation of test.go/testx.go required: can't mix C definitions with //export
- Tests remain sorted by issue number
- Platform-specific code uses build tags

For #26473