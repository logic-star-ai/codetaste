Title
-----
Remove `HirId -> LocalDefId` map from HIR data structure

Summary
-------
Remove the `local_id_to_def_id: SortedMap<ItemLocalId, LocalDefId>` field from `OwnerNodes` in HIR, along with associated lookup methods like `local_def_id(HirId)` and `opt_local_def_id(HirId)`.

Why
---
Having this map in HIR prevents creating new definitions after HIR has been built. The map is redundant and can be eliminated by refactoring code to pass `LocalDefId` directly where needed.

Changes
-------

**Core HIR changes:**
- Remove `local_id_to_def_id` field from `OwnerNodes<'tcx>` struct
- Remove `local_def_id()` and `opt_local_def_id()` methods from HIR map
- Stop populating the map during HIR lowering

**Visitor pattern changes:**
- Change `visit_fn()` signature: `fn_id` parameter from `HirId` → `LocalDefId`
- Update `walk_fn()`, `walk_item()`, `walk_trait_item()`, `walk_impl_item()` accordingly
- Adjust all visitor implementations across compiler/tools

**Query changes:**
- Update `is_late_bound_map` query: parameter `LocalDefId` → `hir::OwnerId`, return type uses `ItemLocalId` instead of `LocalDefId`

**Helper function updates:**
- `associated_body()` now returns `Option<(LocalDefId, BodyId)>` instead of `Option<BodyId>`
- Various utility functions updated to accept/return `LocalDefId`/`OwnerId` instead of `HirId`

**Call site updates:**
- Replace `hir().local_def_id(hir_id)` with direct `LocalDefId`/`OwnerId` usage
- Pass `item.owner_id.def_id`, `trait_item.owner_id.def_id`, etc. directly
- Use `def_id.to_def_id()` instead of `hir().local_def_id(hir_id).to_def_id()`

**Affected areas:**
- AST lowering
- Lints (clippy, rustc lints)
- Type checking
- Trait resolution
- MIR building
- Incremental compilation
- Save-analysis
- rustdoc