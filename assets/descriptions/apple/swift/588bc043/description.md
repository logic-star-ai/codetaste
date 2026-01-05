# Refactor AttrKind enums to use scoped enums and align with DeclKind pattern

## Summary

Refactor `DeclAttrKind` and `TypeAttrKind` to align with other "kind" enums (e.g., `DeclKind`) by converting to scoped enums, standardizing naming conventions, and modernizing metaprogramming patterns.

## Changes

### Scoped Enums
- Convert `DeclAttrKind` to scoped enum: `DAK_Available` → `DeclAttrKind::Available`
- Convert `TypeAttrKind` to scoped enum: `TAK_noescape` → `TypeAttrKind::NoEscape`

### TypeAttrKind Naming
- Use class names instead of spelling as enum case names
- Example: `TAK_noescape` → `TypeAttrKind::NoEscape`, `TAK__opaqueReturnTypeOf` → `TypeAttrKind::OpaqueReturnTypeOf`

### File Organization
- Split `Attr.def` into `DeclAttr.def` and `TypeAttr.def`
- Nothing was handling both attribute kinds simultaneously

### Enum Counting
- Remove `DAK_Count` / `DeclAttrKind::Count`
- Introduce `NumDeclAttrKinds` constant for enum count
- Use `llvm::Optional<DeclAttrKind>` to represent invalid/absent attribute kinds
- Add `LAST_DECL_ATTR` and `LAST_TYPE_ATTR` macros for metaprogramming
- Remove dummy `_counting_TAK_*` symbols

## Impact

- All call sites updated to use scoped enum syntax
- `getAttrKindFromString()` now returns `Optional<DeclAttrKind>` instead of `DAK_Count` on failure
- Better consistency with other "kind" enum patterns in the codebase