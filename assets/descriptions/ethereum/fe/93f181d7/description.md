# Refactor diagnostic system to store salsa IDs and defer message generation

## Summary
Move diagnostic infrastructure from `hir` to `hir-analysis` crate, refactor diagnostic enums to store salsa IDs instead of pre-computed strings, and consolidate all message formatting in `to_complete()` implementations.

## Why
Current diagnostic system constructs messages/labels early via helper functions, which:
- Loses type information and context
- Makes it harder to format context-aware messages
- Prevents leveraging concrete span locations for better error messages (e.g. sorting labels, "defined first here" vs "redefined here")

## What
- Move `DiagnosticVoucher` trait + `analysis_pass` module from `hir` → `hir-analysis`
- Refactor diagnostic enums to store salsa IDs (`TyId`, `IdentId`, `FuncDef`, `ImplTrait`, etc.) instead of pre-formatted strings
- Remove helper constructors that generate strings/messages early
- Consolidate all message formatting logic in `to_complete(&dyn SpannedHirAnalysisDb)` implementations
- Change `DiagnosticVoucher::to_complete()` signature to accept `SpannedHirAnalysisDb` instead of `SpannedHirDb`

## Changes
- **Move files**: `hir/diagnostics.rs` → `hir-analysis/diagnostics.rs`, `hir/analysis_pass.rs` → `hir-analysis/analysis_pass.rs`
- **Update all diagnostic enums**: `NameResDiag`, `TyLowerDiag`, `BodyDiag`, `TraitLowerDiag`, `TraitConstraintDiag`, `ImplDiag`
  - Store typed IDs instead of `String`/messages
  - Remove `message()`, `sub_diags()`, `severity()` helper methods
  - Implement all formatting in `to_complete()`
- **Example**: `BodyDiag::TypeMismatch(span, expected_str, given_str)` → `TypeMismatch { span, expected: TyId, given: TyId }`
- **Removes ~600 LOC** of early string formatting code
- Update `SpannedHirAnalysisDb` trait bound requirements throughout driver/language-server