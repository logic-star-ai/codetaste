# Title
Remove `#[macro_use] extern crate tracing` from rustc crates (round 4)

## Summary
Replace implicit macro importing via `#[macro_use] extern crate tracing` with explicit `use` statements across `rustc_*` crates.

## Why
Explicit importing of macros via `use` items is more standard and readable than implicit importing via `#[macro_use]`. This continues the modernization effort from previous rounds.

## Changes
Remove `#[macro_use] extern crate tracing;` from:
- `rustc_borrowck`
- `rustc_hir_analysis`
- `rustc_hir_typeck`
- `rustc_infer`
- `rustc_mir_transform`
- `rustc_trait_selection`

Add explicit imports throughout affected files:
- `use tracing::{debug, instrument, trace, ...};`
- Import only the macros actually used in each module

## Scope
After this change, no `rustc_*` crates use `#[macro_use] extern crate tracing` except `rustc_codegen_gcc` (handled separately).