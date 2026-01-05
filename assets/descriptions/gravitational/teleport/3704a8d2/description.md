# Title

Refactor tctl commands to use lazy auth client initialization

# Summary

Reorganize tctl command architecture to avoid eagerly initializing auth client connections. Commands now receive a lazy initialization function instead of a pre-connected client, allowing commands that don't need authentication (like `version`) to execute without connecting to the auth server.

# Why

- Commands like `tctl version` were unnecessarily connecting to auth server
- Improved startup performance for non-auth commands
- Better separation of concerns between command logic and auth connection
- Enhanced testability by decoupling command matching from auth initialization

# Changes

**Architecture**:
- Replace `*authclient.Client` parameter with `commonclient.InitFunc` in `CLICommand.TryRun()`
- `InitFunc` returns `(client, closeFunc, error)` for lazy loading
- Commands call `clientFunc(ctx)` only when auth client is actually needed

**New Package Structure**:
- `tool/tctl/common/config/` - configuration handling (`GlobalCLIFlags`, `ApplyConfig`, `LoadConfigFromProfile`)
- `tool/tctl/common/client/` - auth client initialization (`InitFunc`, `GetInitFunc`)

**Command Pattern**:
```go
// Before
func (c *Cmd) TryRun(ctx context.Context, cmd string, client *authclient.Client) (bool, error)

// After  
func (c *Cmd) TryRun(ctx context.Context, cmd string, clientFunc commonclient.InitFunc) (bool, error) {
    client, closeFn, err := clientFunc(ctx)
    // ... use client
    closeFn(ctx)
}
```

**Commands Updated**:
- All 30+ tctl commands refactored to use new pattern
- New `VersionCommand` added that doesn't require auth
- Interface-based clients for better testability (e.g., `authCommandClient`, plugin clients)

**Testing**:
- Added `TestCommandMatchBeforeAuthConnect` to verify commands don't init client during matching
- Updated all existing tests to use mock `InitFunc`