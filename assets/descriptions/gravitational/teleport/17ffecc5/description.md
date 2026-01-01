# Title
Refactor tctl commands to support lazy auth client initialization

# Summary
Reorganize tctl command structure to enable commands that don't require authentication (e.g., `version`) to run without establishing an auth server connection.

# Why
Currently all tctl commands initialize the auth client before determining which command to execute. This forces even simple commands like `tctl version` to connect to the auth server, causing:
- Unnecessary connection overhead
- Commands failing when auth server is unreachable
- Poor user experience for informational commands

# Changes

**Command Interface Refactoring**
- `Initialize()` → now accepts `*tctlcfg.GlobalCLIFlags` parameter
- `TryRun()` → receives `commonclient.InitFunc` instead of `*authclient.Client`
- Commands call init function only when matched, enabling lazy client creation

**New Packages**
- `tool/tctl/common/client` → auth client initialization logic
- `tool/tctl/common/config` → configuration handling (`ApplyConfig`, `LoadConfigFromProfile`, `GlobalCLIFlags`)

**Client Initialization**
- Introduced `InitFunc` type: `func(context.Context) (*authclient.Client, func(context.Context), error)`
- `GetInitFunc()` wraps lazy loading logic
- Clients created on-demand within command execution
- Proper cleanup via returned close function

**Command Pattern**
```go
// Old
func (c *Cmd) TryRun(ctx, cmd, client) { ... client.DoSomething() ... }

// New  
func (c *Cmd) TryRun(ctx, cmd, clientFunc) {
    client, closeFn, err := clientFunc(ctx)
    defer closeFn(ctx)
    ... client.DoSomething() ...
}
```

**Affected Commands**
- All existing commands updated to new pattern
- `VersionCommand` → new standalone command, no auth required
- ~40+ command files modified for consistency

**Testing**
- Added `TestCommandMatchBeforeAuthConnect()` → ensures auth client not initialized during command matching
- Updated integration tests → mock client function signatures

# Benefits
- ✅ Commands run without auth when not needed
- ✅ Faster execution for simple commands
- ✅ Better separation of concerns
- ✅ Consistent error handling via close functions
- ✅ Cleaner code organization