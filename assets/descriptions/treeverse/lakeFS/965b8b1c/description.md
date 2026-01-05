# Simplify config package structure by embedding template

## Summary
Refactor config package to eliminate indirection layer by embedding template structure directly into `Config` struct, allowing direct field access instead of getter methods.

## Changes

- **Embed template into Config**: Merge `configuration` struct from `template.go` directly into `Config` struct in `config.go`, remove intermediate wrapper
- **Direct field access**: Replace getter methods with direct field access throughout codebase (e.g., `cfg.GetListenAddress()` → `cfg.ListenAddress`)
- **Type conversions**: Use Go type conversions for copying config structs to service-specific params where possible
- **Method cleanup**: Remove redundant getter methods, keep only those required by interfaces or performing transformations
- **Rename for clarity**: `GetKVParams()` → `DatabaseParams()`, `GetBlockAdapterS3Params()` → `BlockstoreS3Params()`, etc.

## Why

- Reduces boilerplate code when accessing configuration parameters
- Simplifies config access patterns by making fields public
- Leverages Go's native type conversion for struct copying
- Makes codebase more idiomatic and easier to navigate

## Technical Details

- Deleted `pkg/config/template.go`
- All config fields now public members of `Config` struct
- ~30+ getter methods removed
- Updated all call sites across `cmd/`, `pkg/api/`, `pkg/block/`, `pkg/catalog/`, etc.
- Fixed typo: "reutrns" → "returns"
- Minor cleanup: constants formatting, error handling consistency