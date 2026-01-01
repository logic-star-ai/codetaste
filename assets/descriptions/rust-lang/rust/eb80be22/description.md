# Rename `astconv::AstConv` and related items

## Summary

Large-scale refactoring renaming `astconv::AstConv` trait to `HirTyLowerer` and updating related module, function, and variable names throughout the compiler to reflect that this is HIR type lowering, not AST conversion.

## Changes

### Core Renames

**Module & Trait:**
- `compiler/rustc_hir_analysis/src/astconv/` → `.../hir_ty_lowering/`
- `AstConv` trait → `HirTyLowerer`
- `CreateInstantiationsForGenericArgsCtxt` → `GenericArgsLowerer`

**Main Methods on `HirTyLowerer`:**
- `ast_ty_to_ty` → `lower_ty`
- `ast_region_to_region` → `lower_lifetime`
- `instantiate_*_trait_ref` → `lower_*_trait_ref`
- `get_type_parameter_bounds` → `probe_ty_param_bounds`
- `projected_ty_from_poly_trait_ref` → `lower_assoc_ty`
- `associated_path_to_ty` → `lower_assoc_path`
- `res_to_ty` → `lower_path`
- `hir_id_to_bound_{ty,const}` → `lower_{ty_param,const_param}`
- `ty_of_fn` → `lower_fn_ty`
- `allow_ty_infer` → `allow_infer`
- ... and ~30+ more method renames

**Helper Functions:**
- `convert_{item,trait_item,impl_item,...}` → `lower_*`
- `create_args_for_*` → `lower_generic_args_*`
- `prohibit_assoc_ty_binding` → `prohibit_assoc_item_binding`
- `hir_ty_to_ty` (public API) → `lower_ty`
- ... and many more

**Types:**
- `PathSeg` → `GenericPathSegment`

### Systematic Updates

**Variable naming throughout codebase:**
- `ast_{ty,bounds,generics,trait_ref,fields}` → `hir_*`
- `astconv()` → `lowerer()`

**Documentation & comments:**
- "AST conversion" → "HIR ty lowering"
- "astconv" → "HIR ty lowering" / "lowering"
- Updated all function references in comments

## Rationale

The old naming "AstConv" (AST conversion) was misleading because:
1. It operates on HIR, not AST
2. It performs lowering to `rustc_middle::ty`, not conversion

New naming accurately reflects that this is **HIR type-system entity lowering** to the middle representation.

## Scope

- **No functional changes** - pure refactoring
- **Compiler-wide impact** - touches ~20 files
- Updates rustc, clippy, rustdoc
- Follows MCP 723

## Related

- MCP: rust-lang/compiler-team#723
- rustc-dev-guide PR: rust-lang/rustc-dev-guide#1916