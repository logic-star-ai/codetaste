# Title
-----
Extract `fluent_messages!` macro into separate `rustc_fluent_macro` crate

# Summary
-------
Move the `fluent_messages!` macro from `rustc_macros` into a new dedicated crate `rustc_fluent_macro` to decouple fluent/icu4x dependencies from the core macro infrastructure.

# Why
---
- Fluent + icu4x dependencies take significant time to compile
- `fluent_messages!` is only used by downstream rustc crates
- Currently blocks compilation of upstream crates like `rustc_index` that depend on `rustc_macros` but don't need fluent
- Speeds up `x check compiler` by ~5 seconds

# Changes
-------
**Create new crate:**
- `compiler/rustc_fluent_macro/` with:
  - Move `diagnostics/fluent.rs` from `rustc_macros`
  - Export `fluent_messages!` macro
  - Dependencies: `fluent-bundle`, `fluent-syntax`, `annotate-snippets`, `unic-langid`, proc-macro helpers

**Update `rustc_macros`:**
- Remove fluent-related dependencies from Cargo.toml
- Remove `fluent_messages` export
- Keep other diagnostic macros (`Diagnostic`, `Subdiagnostic`, etc.)

**Update all consumers:**
- Replace `rustc_macros::fluent_messages` → `rustc_fluent_macro::fluent_messages`
- Add `rustc_fluent_macro` dependency to ~30 compiler crates that use `fluent_messages!`
- Update test files accordingly