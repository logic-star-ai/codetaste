# Reorganize 32 issue-based tests into categorized subdirectories

## Summary

Move 32 tests from `tests/ui/issues/` to appropriate topical subdirectories under `tests/ui/` and rename them with descriptive names that reflect their purpose.

## Why

Tests in `tests/ui/issues/` are named after issue numbers (e.g., `issue-23442.rs`, `issue-91489.rs`), making it difficult to understand their purpose without reading the content. Organizing by topic and using descriptive names improves discoverability and maintainability.

## Changes

- **Relocate** 32 tests from `tests/ui/issues/` to categorized subdirectories:
  - `associated-types/`, `autoref-autoderef/`, `binding/`, `cast/`, `closures/`, `coercion/`, `const-generics/`, `cross-crate/`, `deref/`, `drop/`, `editions/`, `enum-discriminant/`, `enum/`, `imports/`, `iterators/`, `lifetimes/`, `lint/`, `loops/`, `macros/`, `mismatched_types/`, `packed/`, `pattern/`, `static/`, `structs/`, `thread-local/`, `typeck/`, `uninhabited/`

- **Rename** tests descriptively:
  - `issue-9725.rs` → `struct-destructuring-repeated-bindings-9725.rs`
  - `issue-91489.rs` → `auto-deref-on-cow-regression-91489.rs`
  - `issue-9942.rs` → `constant-expression-cast-9942.rs`
  - ... (and 29 more)

- **Add** issue URLs at bottom of test files (preserves stderr line numbers)
- **Update** corresponding `.stderr` and `.fixed` files
- **Update** auxiliary crate references (e.g., `issue-9155.rs` → `aux-9155.rs`)

## Methodology

1. Consult `tests/ui/SUMMARY.md` for category structure
2. Determine appropriate category using original issue thread + test content
3. Add issue URL at bottom (not top, to avoid breaking stderr line numbers)
4. Rename with descriptive, purpose-revealing name