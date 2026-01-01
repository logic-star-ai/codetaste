Title
-----
Remove redundant `u32` indices from `BrAnon` and `BoundTyKind::Anon`, store `BoundVar` in `Placeholder` types

Summary
-------
Refactor internal representation of anonymous bound regions and types by removing duplicate index information and consolidating bound variable data into `Placeholder` types.

Changes
-------
- `BrAnon(u32, Option<Span>)` → `BrAnon(Option<Span>)`
- `BoundTyKind::Anon(u32)` → `BoundTyKind::Anon`
- `Placeholder<T>` field renamed: `name: T` → `bound: T` where:
  - `PlaceholderRegion` now stores `bound: BoundRegion` (full bound region) instead of `name: BoundRegionKind`
  - `PlaceholderType` now stores `bound: BoundTy` (full bound type) instead of `name: BoundTyKind`
  - `PlaceholderConst` keeps `bound: BoundVar` (was `name: BoundVar`)

Why
---
The `u32` indices in `BrAnon` and `BoundTyKind::Anon` were redundant with the `BoundVar` already stored in `BoundRegion::var` and `BoundTy::var`. This refactoring:

- Eliminates duplicate information
- Simplifies the type structure
- Makes `Placeholder` types more consistent by storing complete bound variable information
- Provides better access to bound variable metadata through the `BoundVar` field

Impact
------
Updates across compiler:
- Pattern matching on `BrAnon` and bound type kinds
- Construction of placeholder types in canonicalization, higher-ranked trait bounds, and type folding
- Error reporting and pretty printing that accessed the removed indices
- Test output reflecting simplified internal representation