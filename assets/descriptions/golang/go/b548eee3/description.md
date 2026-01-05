# Refactor poller into new internal/poll package

## Summary
Extract poller functionality from `net` package into new `internal/poll` package to enable reuse by `os` package.

## Changes
- **Create `internal/poll` package** with extracted poller code:
  - `FD` type with platform-specific implementations (Unix, Windows, Plan 9)
  - File descriptor mutex (`fdMutex`)
  - Polling runtime hooks (`fd_poll_*.go`)
  - I/O operations: Read, Write, Accept, Connect, etc.
  - Sendfile implementations for multiple platforms
  - Socket options handling
  - Writev support
  - Error types: `ErrClosing`, `ErrTimeout`, `TimeoutError`

- **Update `net` package** to use `internal/poll`:
  - Embed `poll.FD` in `netFD` structure
  - Delegate I/O ops to `poll.FD` methods
  - Replace `net.errTimeout`/`net.errClosing` with `poll.ErrTimeout`/`poll.ErrClosing`
  - Update function signatures and call sites

- **Platform-specific files moved**:
  - `fd_unix.go`, `fd_windows.go`, `fd_plan9.go`
  - `fd_poll_*.go` (runtime, nacl)
  - `sendfile_*.go` (BSD, Linux, Solaris, Windows)
  - `sockopt*.go` (POSIX, platform-specific variants)
  - Hook files for testing

- **Runtime linknames updated**:
  - `net.runtime_*` → `internal/poll.runtime_*`
  - Affects `netpoll.go`, `sema.go`, `time.go`, `net_plan9.go`

- **Dependency updates**:
  - `cmd/dist/deps.go`: Add `internal/poll` to dependency lists
  - `go/build/deps_test.go`: Update package dependency graph
  - `cmd/go/internal/work/build.go`: Add `internal/poll` to race detector list

## Why
Enables `os` package to use poller without depending on `net` package. Large-scale code movement with **no behavioral changes intended**.

## Related Issues
Updates #6817, #7903, #15021, #18507