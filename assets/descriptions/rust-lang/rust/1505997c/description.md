Title
-----
Replace `rustc_target` with `rustc_abi` imports across compiler crates

Summary
-------
Refactor compiler crates to directly use `rustc_abi` instead of `rustc_target` for ABI-related types. Apply systematic substitutions:
- `rustc_target::spec::abi::Abi` → `rustc_abi::ExternAbi`
- `rustc_target::abi::call` → `rustc_target::callconv`
- `rustc_target::abi` → `rustc_abi`

Why
---
Reexports confound module organization. Using `rustc_abi` directly clarifies where ABI types originate and improves code maintainability.

What Changed
------------
- Updated imports in: `rustc_codegen_llvm`, `rustc_codegen_ssa`, `rustc_const_eval`, `rustc_hir_analysis`, `rustc_hir_typeck`, `rustc_lint`, `rustc_metadata`, `rustc_middle`, `rustc_mir_dataflow`, `rustc_mir_transform`, `rustc_pattern_analysis`, `rustc_session`, `rustc_smir`, `rustc_symbol_mangling`, `rustc_ty_utils`
- Removed `rustc_middle::ty::ReprOptions` reexport (use `rustc_abi::ReprOptions` directly)
- Tightened import discipline in `rustc_middle::ty::layout` module
- Updated `Cargo.toml` dependencies accordingly

Out of Scope
------------
Explicitly **excludes**:
- `rustc_passes` crate
- AST crates
- `rustc_abi` crate itself
- `rustc_target` crate

(These will be addressed separately due to stability checking considerations)