# Refactor command setup

## Summary
Refactor gopass subcommand configuration to simplify future changes to command structure. Move command definitions from centralized location into module-specific `GetCommands()` functions.

## Changes

### Command Registration
- Moved command definitions from `commands.go` into separate modules:
  - `pkg/action/commands.go` - core commands (audit, clone, config, copy, delete, edit, find, etc.)
  - `pkg/action/binary/commands.go` - binary operations (cat, sum, copy, move)
  - `pkg/action/create/commands.go` - secret creation wizard
  - `pkg/action/xc/commands.go` - experimental crypto commands
- Each module exports `GetCommands()` returning `[]*cli.Command`
- Commands are aggregated and sorted alphabetically in `getCommands()`

### Context Handling
- Action method signatures changed: `(ctx context.Context, c *cli.Context)` → `(c *cli.Context)`
- Each action extracts context via `ctx := ctxutil.WithGlobalFlags(c)`
- Removed `withGlobalFlags()` helper from `main.go`
- Added `ctxutil.WithGlobalFlags(c *cli.Context) context.Context` for global flag parsing
- `setupApp()` now returns `(context.Context, *cli.App)` instead of just `*cli.App`
- App runs via `app.RunContext(ctx, os.Args)` instead of `app.Run(os.Args)`

### Test Updates
- All tests updated to set `c.Context = ctx` before calling action methods
- CLI context now carries the Go context throughout the call chain

## Why
- Decentralizes command definitions, making them easier to locate and modify
- Simplifies adding/removing commands in specific modules
- Standardizes context propagation pattern across all actions
- Reduces boilerplate in command setup
- Prepares codebase for future command structure changes