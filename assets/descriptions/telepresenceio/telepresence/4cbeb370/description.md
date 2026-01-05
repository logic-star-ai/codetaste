# Refactor CLI package structure

## Summary
Restructure `pkg/client/cli` and eliminate the `cli/util` anti-pattern package. Move code into semantically meaningful packages with consistent naming conventions.

## Why
- Current structure has evolved over 2+ years into "spaghetti-like" organization
- Package name `util` violates Go best practices (go.dev/blog/package-names)
- Inconsistent naming of types and functions
- Poor separation of concerns
- Code hygiene needed before adding features like `--docker` option

## Changes

### New package structure
```
cli/
├── cmd/           # All command definitions (connect, status, list, intercept, ...)
├── cloud/         # Cloud messaging & update checks
├── connect/       # Connection/session management
├── daemon/        # Daemon client & request handling  
├── flags/         # Flag parsing utilities
└── intercept/     # Intercept-specific logic
```

### Eliminated
- `cli/util/` package entirely

### Renamed
- `cmd_*.go` → `cmd/*.go` (removed prefix, moved to subpackage)
- `cloudMessageCache` → `messageCache`
- `UpdateChecker` → `updateChecker` (unexported)
- `UserDaemon` → `daemon.UserClient`
- Various command structs for consistency

### Moved
- Cloud messaging: `util/cloud_*.go` → `cloud/`
- Update checks: `util/update_check.go` → `cloud/`
- Connection logic: `util/{connector,daemon,init_command}.go` → `connect/`
- Daemon client: types → `daemon/userd.go`
- Request handling: `connect/request.go` → `daemon/request.go`
- Intercept utilities: `util/{describe_intercepts,prepare_mount}.go` → `intercept/`
- Flag utilities: `util/flags*.go` → `flags/`
- All commands: `cmd_*.go` → `cmd/*.go`

## Notes
- **No logic changes** — pure refactoring
- Testdata moved with corresponding test files
- Better encapsulation (many types/functions now unexported)