# Title
Rename `runtime` package to `daemon` throughout codebase

## Summary
Large-scale refactoring to rename the `runtime` package/directory to `daemon` for improved semantic clarity and consistency.

## Changes

### Directory Structure
- Move `runtime/*` → `daemon/*`
- Includes all subdirectories: `execdriver/`, `graphdriver/`, `networkdriver/`

### Code Changes
- Rename `Runtime` struct → `Daemon`
- Update all import paths: `github.com/dotcloud/docker/runtime` → `github.com/dotcloud/docker/daemon`
- Rename package declaration: `package runtime` → `package daemon`

### Variable/Function Renaming
- `runtime` variables → `daemon`
- `globalRuntime` → `globalDaemon`
- `mkRuntime()` → `mkDaemon()`
- `mkRuntimeFromEngine()` → `mkDaemonFromEngine()`
- `NewRuntime()` → `NewDaemon()`
- `NewRuntimeFromDirectory()` → `NewDaemonFromDirectory()`
- ...and similar patterns throughout

### Comments/Documentation
- Update comments referencing "runtime" to "daemon" where appropriate
- Update error messages and log statements

## Files Affected
- Core: `daemon/{container,daemon,volumes,utils,...}.go`
- Drivers: `daemon/{execdriver,graphdriver,networkdriver}/**/*`
- Tests: `integration/*_test.go`
- API: `builtins/`, `server/`, `daemonconfig/`, `graph/`, `image/`
- Build files with conditional compilation tags

## Scope
Purely nomenclature change - **no functional modifications**. All logic remains identical.