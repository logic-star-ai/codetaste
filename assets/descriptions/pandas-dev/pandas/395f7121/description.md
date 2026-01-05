# Rename isnull → isna, notnull → notna for API consistency

## Summary
Rename `isnull()` to `isna()` and `notnull()` to `notna()` across pandas codebase to achieve consistent naming with existing methods like `dropna()` and `fillna()`.

## Changes

### Core API
- Add top-level functions `isna()` and `notna()` as new canonical names
- Maintain `isnull()` and `notnull()` as aliases for backward compatibility
- Add `.isna()` / `.notna()` methods to all classes: `Series`, `DataFrame`, `Index`, `Categorical`, `Panel`, etc.
- Keep `.isnull()` / `.notnull()` as aliases on all classes

### Configuration
- Deprecate `mode.use_inf_as_null` option
- Add `mode.use_inf_as_na` as replacement with identical behavior

### Internal Implementation
- Rename internal functions: `_isnull*` → `_isna*` (e.g., `_isnull_new` → `_isna_new`)
- Rename lib functions: `isnullobj*` → `isnaobj*` 
- Update all internal usages throughout codebase to use new names

### Documentation
- Update all documentation, examples, and tutorials to use `isna`/`notna`
- Update API reference pages
- Update comparison guides (SQL, SAS, etc.)

### Testing
- Update test suite to use new naming convention
- Ensure aliases work correctly
- Verify backward compatibility

## Why
Achieve consistent naming convention across the API - methods already named with `*na` pattern (`dropna`, `fillna`) should align with null-checking functions.