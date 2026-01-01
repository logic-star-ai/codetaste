# Refactor: Move `mir::Field` to `abi::FieldIdx`

## Summary

Move the `Field` type from `rustc_middle::mir` to `rustc_abi` and rename it to `FieldIdx`. Update all imports and usages throughout the codebase accordingly.

## Why

`Field` represents the source-order index of fields in variants, which is fundamentally an ABI concern rather than a MIR-specific concept. The type should live in `rustc_abi` alongside other index types like `VariantIdx`.

## Changes

- Move `Field` newtype definition from `compiler/rustc_middle/src/mir/mod.rs` to `compiler/rustc_abi/src/lib.rs`
- Rename `Field` → `FieldIdx` for consistency with `VariantIdx` and other ABI types
- Update imports: `use rustc_middle::mir::Field` → `use rustc_target::abi::FieldIdx`
- Mechanically replace `Field::new(...)` → `FieldIdx::new(...)` throughout codebase
- Update type signatures, pattern matches, and other references

## Affected Areas

- `rustc_abi`, `rustc_middle`, `rustc_mir_build`, `rustc_mir_transform`, `rustc_mir_dataflow`
- `rustc_borrowck`, `rustc_codegen_cranelift`, `rustc_codegen_llvm`, `rustc_codegen_ssa`
- Type checking, pattern matching, drop elaboration, THIR lowering, value analysis, ... 

## Notes

This is purely a move-and-rename refactoring. Future work will remove unnecessary `FieldIdx::new` calls and use `FieldIdx` more idiomatically.