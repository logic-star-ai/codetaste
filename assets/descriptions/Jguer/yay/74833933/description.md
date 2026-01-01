# Title
Refactor: Invert configuration-runtime relationship and eliminate global logger

# Summary
Major architectural refactoring that inverts the relationship between Configuration and Runtime, eliminates global logger dependencies, and reorganizes code into clearer package boundaries. Runtime now owns Configuration instead of Configuration owning Runtime, and all logging is explicitly dependency-injected.

# Why
- **Better dependency management**: Runtime as top-level orchestrator with injected dependencies
- **Improved testability**: Eliminate global state (logger) making tests more isolated
- **Clearer architecture**: Separate runtime state from static configuration
- **Better package organization**: Code moved to appropriate domain packages (`sync`, `build`, `srcinfo`, etc.)

# Changes

## Architecture
- **Invert cfg/runtime relationship**: `runtime.Runtime` now contains `Cfg *settings.Configuration` instead of `cfg.Runtime`
- **Remove global logger**: Eliminate `text.GlobalLogger` and all global logging methods (`text.Errorln()`, `text.Infoln()`, etc.)
- **Explicit dependency injection**: Logger passed through Runtime → services → functions

## Package Reorganization
- Move `pkg/settings/runtime.go` → `pkg/runtime/runtime.go`
- Create `pkg/sync` package with:
  - `pkg/sync/build` (installer logic from `aur_install.go`)
  - `pkg/sync/srcinfo` (from `pkg/srcinfo` + `pkg/pgp`)
  - `pkg/sync/workdir` (preparer, aur_source from root)
- Move operator logic → `pkg/sync/sync.go`

## API Changes
- Functions take `*runtime.Runtime` instead of `*settings.Configuration`
- `text.GetInput(...)` → `logger.GetInput(...)`
- `text.ContinueTask(...)` → `logger.ContinueTask(...)`
- `download.PKGBUILDs(...)` + logger param
- `download.PKGBUILDRepos(...)` + logger param
- `news.PrintNewsFeed(...)` + logger param

## Error Handling
- Move build-specific errors → `pkg/sync/build/errors.go`
- Remove global error types from root `errors.go`

## Code Quality
- Add `forbidigo` linter rule to prevent `fmt.Print*` commits
- Update golangci-lint Go version → 1.20
- Better test isolation with explicit logger creation
- Remove outdated FAQ entries from README

## File Movements
```
aur_install.go → pkg/sync/build/installer.go
preparer.go → pkg/sync/workdir/preparer.go
aur_source.go → pkg/sync/workdir/aur_source.go
install.go → pkg/sync/build/pkg_archive.go (partial)
pkg/pgp/* → pkg/sync/srcinfo/pgp/*
pkg/srcinfo/* → pkg/sync/srcinfo/*
```