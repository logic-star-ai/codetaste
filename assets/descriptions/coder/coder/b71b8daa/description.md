Title
-----
Convert entire CLI from Cobra to clibase

Summary
-------
Replaced `spf13/cobra` with custom `clibase` framework across all CLI commands, subcommands, and tests. Removed `cliflag` package and migrated all flag/option handling to `clibase.OptionSet`.

Why
---
- Need more control over CLI behavior than cobra/viper offers
- Enable better YAML configuration support
- Improve flag precedence and inheritance handling
- Better error formatting and context
- Foundation for future improvements (telemetry, dynamic docs generation, etc.)

What Changed
------------

**Core CLI Structure**
- All `*cobra.Command` → `*clibase.Cmd`
- `RunE func(*cobra.Command, []string)` → `Handler func(*clibase.Invocation)`
- Options now defined declaratively via `clibase.OptionSet` instead of imperative flag registration
- Commands moved to methods on `RootCmd` struct (e.g., `create()` → `(r *RootCmd) create()`)

**Flag/Option Handling**
- Removed entire `cliflag` package
- Environment variable consumption built into `clibase.Option`
- Default values, env vars, descriptions all defined in option struct
- Better handling of array flags and defaults

**Testing Infrastructure**
- `clitest.New()` returns `(*clibase.Invocation, config.Root)` instead of `(*cobra.Command, config.Root)`
- New `clitest.Start()` for better lifecycle management
- New `clitest.StartWithWaiter()` for async execution with error capture
- `clitest.Run()` for synchronous execution
- Improved cleanup via `t.Cleanup()` integration

**Documentation Generation**
- Updated `scripts/clidocgen/` to work with clibase
- New template system for CLI docs
- Regenerated all CLI documentation in `docs/cli/`

**Agent & Server**
- Agent command converted to clibase
- Server command already using clibase, fully integrated
- Provisioner daemon command converted

**Enterprise Commands**
- All enterprise subcommands (groups, licenses, features) converted
- Moved to methods on `enterprise/cli.RootCmd`

Breaking Changes
---------------
- `FormatCobraError` removed (error formatting built into clibase)
- `cliflag` package completely removed
- Command initialization now requires calling `PrepareAll()`

Affected Areas
--------------
- All files in `cli/` (100+ commands)
- All files in `enterprise/cli/`
- Test helpers in `cli/clitest/`
- Documentation generation in `scripts/clidocgen/`
- All CLI tests across codebase
- `pty/ptytest` integration