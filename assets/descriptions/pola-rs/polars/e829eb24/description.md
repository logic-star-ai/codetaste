# Remove `polars(_core)::export` module and make dependencies explicit

## Summary
Remove the `export` module from `polars-core` and `polars` crates. All crates should specify their own dependencies directly instead of accessing them through re-exports.

## Why
The `export` module is an archaic leftover from before all crates were part of the workspace. It creates implicit dependencies and makes the dependency graph unclear.

## What
- Delete `polars-core/src/export.rs` (exported `chrono`, `regex`, `serde`, `arrow`, `num_traits`, `once_cell`, `rayon`, `_boost_hash_combine`)
- Delete `polars/src/export.rs` (re-exported `polars_core::export::*`)
- Update all imports across codebase:
  - `polars_core::export::chrono::*` → `chrono::*`
  - `polars_core::export::num::*` → `num_traits::*`
  - `polars_core::export::rayon::*` → `rayon::*`
  - `polars_core::export::regex::*` → `regex::*`
  - `polars_core::export::arrow::*` → `arrow::*`
  - `polars_core::export::once_cell::*` → `once_cell::*`
  - `polars_core::export::cast::*` → `polars_compute::cast::*`
  - `polars_core::export::_boost_hash_combine` → `polars_utils::hashing::_boost_hash_combine`
- Add explicit dependencies to Cargo.toml files:
  - `chrono` → polars-lazy, polars-ops, polars-python, polars
  - `once_cell` → polars-ops, polars-pipe
  - `regex` → polars-sql
  - `num-traits` → polars-time
  - `rayon` → polars-time, polars-python
  - `polars-arrow` → polars-python
  - `polars-compute` → polars-python
- Move `_boost_hash_combine` from `polars-core/src/hashing/mod.rs` to `polars-utils/src/hashing.rs`
- Update all references across ~40+ files in polars-ops, polars-python, polars-sql, polars-time, polars-pipe, polars-plan, polars-expr, polars-lazy, etc.

## Impact
Each crate now has explicit, clear dependencies rather than transitive access through re-exports.