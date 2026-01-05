# Title

Remove enum variant glob-imports from `rustc_middle::ty`

# Summary

Replace glob-imported enum variants with fully qualified `EnumName::Variant` style throughout the compiler codebase.

# Why

The compiler used an idiom where enum variants were prefixed/suffixed (e.g., `BrAnon`, `BrNamed` for `BoundRegionKind`) and then glob-imported directly. Using the standard `EnumName::Variant` style is easier to read and more consistent with Rust conventions.

# Changes

**Rename enum variants** for better clarity:
- `BoundRegionKind`: `BrAnon` → `Anon`, `BrNamed` → `Named`, `BrEnv` → `ClosureEnv`
- `BorrowKind`: `Imm` → `Immutable`, `MutBorrow` → `Mutable`, `UniqueImmBorrow` → `UniqueImmutable`
- `AssocItemContainer`: `TraitContainer` → `Trait`, `ImplContainer` → `Impl`

**Update usage** across:
- `rustc_borrowck/*` ... borrow checking, diagnostics, type checking
- `rustc_hir_analysis/*` ... HIR analysis, intrinsics, WF checking
- `rustc_hir_typeck/*` ... type checking, method probing, upvar analysis
- `rustc_trait_selection/*` ... trait selection, coherence, error reporting
- `rustc_infer/*`, `rustc_middle/*`, `rustc_ty_utils/*` ... type system core
- Clippy, rustdoc, tests ... downstream consumers

**Remove glob-imports**:
- `use ty::BoundRegionKind::*;`
- `use ty::BorrowKind::*;`
- etc.

# Notes

- Test output updated to reflect new variant names
- No functional changes, purely naming/style refactoring
- Slightly longer names (e.g., `Immutable` vs `Imm`) acceptable given infrequent usage