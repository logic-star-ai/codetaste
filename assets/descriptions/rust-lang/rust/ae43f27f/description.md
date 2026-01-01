# Refactoring Task: Rename "object safe" to "dyn compatible" in compiler

## Summary

Rename all occurrences of "object safe"/"object safety" terminology to "dyn-compatible"/"dyn-compatibility" throughout the Rust compiler codebase, following completed T-lang FCP.

## Scope

### Rename the following:

**Queries:**
- `object_safety_violations` → `dyn_compatibility_violations`
- `is_object_safe` → `is_dyn_compatible`

**Types:**
- `ObjectSafetyViolation` → `DynCompatibilityViolation`
- `ObjectSafetyViolationSolution` → `DynCompatibilityViolationSolution`

**Error Messages:**
- Update all diagnostics from "object safe"/"object-safe" → "dyn-compatible"
- Update help text: "if this is an object-safe trait" → "if this is a dyn-compatible trait"
- Update notes: "for a trait to be object safe" → "for a trait to be dyn-compatible"

**Predicates:**
- `PredicateKind::ObjectSafe` → `PredicateKind::DynCompatible`
- `SelectionError::TraitNotObjectSafe` → `SelectionError::TraitDynIncompatible`

**Module/File Names:**
- `object_safety.rs` → `dyn_compatibility.rs`

**Functions & Methods:**
- `trait_is_object_safe` → `trait_is_dyn_compatible`
- `hir_ty_lowering_object_safety_violations` → `hir_ty_lowering_dyn_compatibility_violations`
- `object_safety_violations_for_*` → `dyn_compatibility_violations_for_*`
- `report_object_safety_error` → `report_dyn_incompatibility`

**Comments & Documentation:**
- Update all inline comments, doc comments, and error code documentation
- Update references in `E0038.md` and related error codes
- Add footnotes: `[^1]: Formerly known as "object-safe"`

**Test Files:**
- Update test names in `tests/ui/object-safety/...`
- Update all `.stderr` files with new error messages

## Excluded

- `compiler/rustc_codegen_cranelift` (separate PR)
- Feature flag names (add FIXME comments for future rename)

## Notes

- Follow-up required for relnotes tracking issue
- Some URLs still reference old "object-safety" documentation (add FIXME)
- Preserve backwards compatibility where needed via footnotes/comments