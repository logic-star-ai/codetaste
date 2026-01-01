# Title
-----
Consolidate git command execution to use `Run(&RunOpts{})` pattern

# Summary
--------
Standardize git command execution by removing deprecated `Run`, `RunInDir*` methods and consolidating to three main functions: `Run`, `RunStdString`, `RunStdBytes` with `RunOpts{}` parameter.

# Why
---
Multiple redundant methods for running git commands (`Run()`, `RunInDir()`, `RunInDirBytes()`, `RunInDirWithEnv()`, `RunWithContext()`, etc.) created API inconsistency and confusion.

# Changes
---------
- Rename `RunContext` → `RunOpts`
- Rename `RunWithContext(&RunContext{...})` → `Run(&RunOpts{...})`
- Remove `Run()`, `RunInDir()`, `RunInDirBytes()`, `RunInDirWithEnv()`
- Replace with `RunStdString(&RunOpts{...})`, `RunStdBytes(&RunOpts{...})`, `Run(&RunOpts{...})`

# Migration Pattern
------------------
```go
// Before
stdout, err := cmd.RunInDir(path)
stdout, err := cmd.RunInDirWithEnv(path, env)
stdout, err := cmd.Run()
err := cmd.RunWithContext(&RunContext{...})

// After
stdout, _, err := cmd.RunStdString(&RunOpts{Dir: path})
stdout, _, err := cmd.RunStdString(&RunOpts{Dir: path, Env: env})
stdout, _, err := cmd.RunStdString(nil)
err := cmd.Run(&RunOpts{...})
```

# Files Changed
--------------
- `modules/git/command.go` - Core API changes
- `cmd/`, `integrations/`, `modules/`, `routers/`, `services/` - Update all callers
- Remove `Timeout: -1` boilerplate (now default)