# Rename `rustc_abi::Abi` to `BackendRepr`

## Summary

Rename `rustc_abi::Abi` enum to `BackendRepr` and rename the `Aggregate` variant to `Memory`. This addresses long-standing confusion between backend representation and actual calling conventions.

## Why

The `Abi` type never actually represented how values are passed between functions (which requires `PassMode` consideration). Instead, it only describes how values are represented to the codegen backend (e.g., as scalars, scalar pairs, or memory).

This conflation arose because LLVM, the primary backend, would lower certain IR forms using certain ABIs. However, this relationship breaks down with:
- Different architectures
- ABI-modifying IR annotations  
- Same architecture with different ISA extensions enabled
- ...other edge cases

## Changes

- `rustc_abi::Abi` → `rustc_abi::BackendRepr`
- `Abi::Aggregate { sized }` → `BackendRepr::Memory { sized }`
- Updated all references throughout:
  - `rustc_codegen_*`
  - `rustc_const_eval`
  - `rustc_mir_*`
  - `rustc_ty_utils`
  - ...etc
- Added documentation clarifying the distinction
- Updated test expectations

## Notes

- This is **not a complete fix**, just a step to prevent further confusion
- Both names are still somewhat imprecise due to years of code written based on the misunderstanding
- Proper resolution requires disentangling significant amounts of duplicated backend code
- `Memory` is also a misnomer (sometimes uses IR aggregates instead)