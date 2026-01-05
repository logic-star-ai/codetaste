Title
-----
Complete `RegionKind` renaming: `ReEarlyBound` → `ReEarlyParam`, `ReFree` → `ReLateParam`

Summary
-------
Rename region kinds and related types to use more descriptive terminology:
- `ReEarlyBound` → `ReEarlyParam`
- `ReFree` → `ReLateParam`
- `EarlyBoundRegion` → `EarlyParamRegion`
- `FreeRegion` → `LateParamRegion`
- `RegionNameSource::NamedEarlyBoundRegion` → `NamedEarlyParamRegion`
- `RegionNameSource::NamedFreeRegion` → `NamedLateParamRegion`
- `infer::EarlyBoundRegion` → `RegionParameterDefinition`

Update `CheckRegions` enum:
- `OnlyEarlyBound` → `OnlyParam`
- `Bound` → `FromFunction`

Rename methods:
- `lub_free_regions` → `lub_param_regions`
- `is_free_or_static` → `is_free` (with updated semantics)

Why
---
Current naming conflates different concepts and is confusing:
- "Bound" vs "Free" terminology doesn't clearly convey early vs late parameter distinction
- `ReFree` despite being called "free" represents late-bound function parameters after liberation
- `is_free_or_static` mixes parameter regions with `'static`

New naming:
- **`ReEarlyParam`**: Region parameters from type/trait definitions (`'a` in `impl<'a>`)
- **`ReLateParam`**: Late-bound function parameters after liberation (formerly `ReFree`)
- **`EarlyParamRegion`/`LateParamRegion`**: Corresponding struct names
- Aligns with existing `ty::Param` for type parameters

Changes
-------
- Update all region kind discriminants and pattern matching
- Adjust region classification methods (`is_free`, `is_param`)
- Update diagnostics and error messages referencing region types
- Revise comments/docs to reflect early vs late-bound distinction
- Rename `CheckRegions` variants to clarify usage (params vs function contexts)

Implementation
--------------
- Mechanical rename across borrowck, hir_analysis, infer, middle, trait_selection
- Update stable_mir and clippy for new terminology
- Preserve all existing behavior; pure refactoring
- Update test error messages with new internal region repr