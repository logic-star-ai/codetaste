# Remove trait `DefIdTree`

## Summary
Remove the `DefIdTree` trait abstraction and move its methods directly into `TyCtxt` implementation.

## Why
The `DefIdTree` trait was designed to generalize over both `TyCtxt` and `Resolver`, but since `Resolver` now has access to `TyCtxt`, this abstraction layer is redundant and adds unnecessary complexity.

## Changes
- Remove `DefIdTree` trait definition from `rustc_middle::ty`
- Move trait methods (`opt_parent`, `parent`, `opt_local_parent`, `local_parent`, `is_descendant_of`) directly to `TyCtxt` impl block
- Update `Visibility::{is_accessible_from, is_at_least}` to accept `TyCtxt<'_>` instead of `impl DefIdTree`
- Remove `impl DefIdTree for TyCtxt` and `impl DefIdTree for &Resolver`
- Remove all `DefIdTree` imports across compiler crates
- Update call sites throughout rustc/clippy/rustdoc to use `TyCtxt` directly

## Impact
- Simplifies type signatures and trait bounds
- Eliminates ~100+ `DefIdTree` import statements
- Makes API surface clearer by removing indirection