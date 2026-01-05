# Refactor: Rename `Substs` to `GenericArgs` throughout compiler

## Summary

Rename `Substs`/`SubstsRef`/`InternalSubsts` to `GenericArgs`/`GenericArgsRef` throughout the compiler to use terminology consistent with how generics are referred to in the language.

## Changes

- Rename `SubstsRef` → `GenericArgsRef<'tcx>`, `InternalSubsts` → `GenericArgs<'tcx>`
- Rename variables/fields: `substs` → `args` throughout codebase
- Rename module: `ty::subst` → `ty::generic_args` (made private, re-export content in `ty` module)
- Rename methods: `EarlyBinder::subst(_identity)` → `EarlyBinder::instantiate(_identity)`
- Rename types: `*Substs` → `*Args` (e.g., `ClosureSubsts` → `ClosureArgs`, `GeneratorSubsts` → `GeneratorArgs`)
- Rename functions: functions containing `substs` now use `args` or `generic_args`

## Affected Areas

- `rustc_borrowck/` ... constraint generation, diagnostics, type checking
- `rustc_codegen_*` ... callee resolution, intrinsics, mono items
- `rustc_const_eval/` ... const evaluation, interpretation
- `rustc_middle/` ... core type definitions
- `rustc_hir_analysis/` ... HIR analysis
- Clippy lints ... method checking, type utilities
- Miri ... interpretation
- Tests ... error messages, THIR/MIR dumps

## Note

The verb "substituting" still appears in comments/documentation. This can be addressed separately as part of #110254 by changing to `replace_generics` or similar terminology.