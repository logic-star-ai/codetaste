Title
-----
Internalize `i18n`, `docsgen`, and `client_example` modules

Summary
-------
Move three golang modules from public API to internal:
- `i18n` → `internal/i18n`
- `docsgen` → `internal/docsgen`  
- `client_example` → `rpc/internal/client_example`

Update all import paths across codebase (commands/*, internal/*, main.go, version/*, ...).

Why
---
Preparation for 1.0.0 release - expose only `commands` and `rpc` packages as public API (1:1 with gRPC interface).

These modules are implementation details not intended for external consumption.

Changes
-------
**Module Moves:**
- `i18n/**` → `internal/i18n/**` (translation/localization system)
- `docsgen/main.go` → `internal/docsgen/main.go` (CLI docs generator)
- `client_example/**` → `rpc/internal/client_example/**` (gRPC example)

**Import Updates:**
- Update ~50+ import statements across commands/*, internal/arduino/*, internal/cli/*
- Replace `github.com/arduino/arduino-cli/i18n` → `.../internal/i18n`
- Replace `github.com/arduino/arduino-cli/docsgen` → `.../internal/docsgen`

**Configuration Updates:**
- Update `.github/workflows/*` paths
- Update `Taskfile.yml` (i18n tasks, cli-docs generation paths)
- Update `.gitignore` patterns
- Update `docs/*.md` references to client_example

**Documentation:**
- Add to `UPGRADING.md` breaking changes list
- Update getting-started, integration-options docs with new paths

Breaking
--------
⚠️ **Breaking change** - external consumers can no longer import these modules.