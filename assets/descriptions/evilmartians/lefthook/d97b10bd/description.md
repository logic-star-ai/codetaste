Title
-----
Restructure internal packages and remove deprecated options

Summary
-------
Refactor internal folder structure and remove long-deprecated CLI flags and config options.

Changes
-------

**Package Restructuring:**
- Rename `internal/lefthook/` → `internal/command/`
- Rename `internal/lefthook/runner/` → `internal/run/`
- Move all runner-related files to flattened `internal/run/` structure
- Rename `Runner` struct → `Run` struct
- Rename `command` interface → `cmd` interface (avoid package name conflict)

**Remove Deprecated Global Flags:**
- Remove `--force` / `-f` from root command
- Remove `--aggressive` / `-a` from root command
- Remove `--aggressive` from `install` and `uninstall` commands
- Remove associated deprecation warnings

**Remove Deprecated Config Options:**
- Remove `remote` field (use `remotes` array)
- Remove `config` field from `Remote` (use `configs` array)
- Remove all backward compatibility code for these options
- Update schema.json accordingly

**Cleanup:**
- Remove `Fs` field from `Options` struct (move to `Lefthook`)
- Remove deprecated `Force` and `Aggressive` fields from `Options`
- Clean up initialization: `Options` no longer needs `afero.Fs`
- Update all tests and test fixtures

Why
---
- Flatten deeply nested folder structures for better navigability
- Remove technical debt from deprecated options that have been warned about for multiple releases
- Simplify codebase by removing backward compatibility code
- Make package names more concise and specific

Breaking Changes
----------------
⚠️ This is a breaking change:
- Global `--force` and `--aggressive` flags removed (use command-specific flags)
- Config fields `remote` and `remote.config` no longer supported
- Must migrate to `remotes[].configs[]` structure