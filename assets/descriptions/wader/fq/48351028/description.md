# Refactor: Update to Go 1.20 and rename internal utility packages

## Summary
Update minimum Go version requirement from 1.18 to 1.20, leverage new standard library features, and rename internal utility packages from `*ex` to `*x` suffix for consistency.

## Changes

### Go Version Update
- Bump minimum required Go version from 1.18 → 1.20
- Update documentation (README.md, go.mod)

### Package Renames
Rename internal utility packages to use `*x` suffix:
- `internal/bitioex` → `internal/bitiox`
- `internal/gojqex` → `internal/gojqx`
- `internal/ioex` → `internal/iox`
- `internal/mathex` → `internal/mathx`
- `internal/sortex` → `internal/sortx`
- `internal/stringsex` → `internal/stringsx`

### Standard Library Migration
Replace custom implementations with Go 1.20 stdlib:
- Remove `internal/cmpex` package entirely
- Use `cmp.Compare` from stdlib instead of custom `cmpex.Compare`
- Use `slices.Sort` instead of `sort.Ints`
- Use `slices.SortFunc` with `cmp.Compare` for custom sorting

### Import Updates
Update all imports across codebase:
- `format/...` packages
- `internal/...` utilities  
- `pkg/...` packages
- All references to renamed packages

## Why
- **Modernization**: Leverage Go 1.20 stdlib improvements (cmp, slices packages)
- **Consistency**: Standardize internal package naming convention (`*x` suffix)
- **Simplification**: Remove custom implementations where stdlib provides equivalent functionality
- **Maintainability**: Reduce codebase surface area by using stdlib