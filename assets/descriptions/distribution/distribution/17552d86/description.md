# Deprecate internal reference package, migrate to extracted module

## Summary

Migrate from internal `reference` package to external `github.com/distribution/reference` module. The reference functionality has been extracted into a standalone module and the internal package is now deprecated with forwarding wrappers.

## Why

- Extract reference handling into reusable, standalone module
- Allow other projects to depend on reference without full distribution dependency
- Improve modularity and maintainability
- Enable independent versioning of reference functionality

## Changes

**Module extraction:**
- New module created at `github.com/distribution/reference` v0.5.0
- Extracted from distribution at commit `b9b19409cf458dcb9e1253ff44ba75bd0620faa6`
- Contains core reference parsing, validation, and manipulation logic

**Import path updates:**
- All imports changed from `github.com/distribution/distribution/v3/reference` → `github.com/distribution/reference`
- Updated across:
  - `blobs.go`, `registry.go`
  - `notifications/*`
  - `registry/api/v2/*`
  - `registry/client/*`
  - `registry/handlers/*`
  - `registry/proxy/*`
  - `registry/storage/*`
  - Test files throughout

**Internal package deprecation:**
- Core implementation files removed (tests, benchmarks, implementation)
- Added deprecation wrapper files:
  - `reference_deprecated.go` - forwards types/funcs
  - `helpers_deprecated.go` - forwards helper funcs
  - `normalize_deprecated.go` - forwards normalization
  - `regexp_deprecated.go` - forwards regex patterns
  - `sort_deprecated.go` - forwards sorting
- All exports now thin wrappers with deprecation notices pointing to new module

**Dependencies:**
- Added `github.com/distribution/reference v0.5.0` to `go.mod`
- Vendored new module with full implementation

## Backward Compatibility

Maintained through deprecation wrappers - existing code using `distribution/v3/reference` continues working but receives deprecation warnings directing to new module.