# Refactor `tbot` CLI architecture for better maintainability and extensibility

## Summary

Refactor the `tbot` CLI to eliminate the global `CLIConf` namespace, improve code organization, and expose new subcommands for various tbot output types and services through pure CLI (not just config files).

## Why

The existing CLI architecture had several issues:
- **Global namespace pollution**: Single `CLIConf` struct used across all commands led to conflicting field definitions and unintended sharing
- **Limited CLI access**: Many tbot features only accessible via config files
- **Poor code organization**: CLI handling mixed with main logic
- **Difficult testing**: Global state made unit testing challenging
- **Flag conflicts**: Shared namespace caused bugs with flag handling (e.g., `--log-format` not working consistently)

## Changes

### New CLI Package Structure
- Move CLI handling to `lib/tbot/cli/` with organized files:
  - `cli.go` - Core types and helpers
  - `globals.go` - Global flags (`GlobalArgs`)
  - `start_*.go` - Start subcommands (identity, database, kubernetes, etc.)
  - `*.go` - Other commands (init, migrate, proxy, etc.)
  - `*_test.go` - Comprehensive tests

### Command Architecture
- Replace `CLIConf` with per-command structs with explicit dependencies
- Introduce `ConfigMutator` interface for commands that modify `BotConfig`
- Implement `genericMutatorHandler` for start/configure commands
- Implement `genericExecutorHandler` for simple action commands
- Create reusable embeddable structs:
  - `sharedStartArgs` - Common flags for modern start/configure subcommands
  - `AuthProxyArgs` - `--auth-server` / `--proxy-server` handling
  - `LegacyDestinationDirArgs` - Legacy `--destination-dir` behavior

### New Subcommands
Expose via CLI:
- `tbot start identity|ssh` - SSH/API access output
- `tbot start database|db` - Database credentials
- `tbot start kubernetes|k8s` - Kubernetes credentials
- `tbot start application|app` - Application credentials
- `tbot start application-tunnel` - App tunnel service
- `tbot start database-tunnel` - DB tunnel service
- `tbot start spiffe-svid` - SPIFFE SVID output
- `tbot start legacy` - Original behavior (default)
- Matching `tbot configure ...` variants for all above

### Testing
- Generic test helpers: `testCommand()`, `testStartConfigureCommand()`
- Unit tests for all commands and argument parsing
- Tests for `GlobalArgs` and shared argument structs
- Tests verify both parsing and config application

### Behavioral Improvements
- `--destination` and `--storage` now accept URIs (`file://`, `memory://`, `kubernetes-secret://`)
- Global flags (e.g., `--log-format`, `--debug`) work consistently across all commands
- No more unintended flag inheritance or conflicts
- Clear separation between legacy and modern flag styles

### Backward Compatibility
- Legacy CLI syntax fully supported via `tbot start legacy` (set as default)
- Existing `tctl bots add` examples continue to work
- Deprecated flags still accepted with warnings

## Implementation Details

**Config Loading**: `LoadConfigWithMutators()` chains mutators to build final config
**Command Pattern**: Commands implement `TryRun()` to handle execution
**Flag Namespacing**: Each command's flags properly scoped, no accidental sharing