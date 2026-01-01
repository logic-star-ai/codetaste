# Rename things in new solver and `rustc_type_ir` for clarity

## Summary

Refactor naming conventions in the trait solver and type infrastructure:
- Rename `interner()` → `cx()` throughout `TypeFolder` and solver
- Rename generic parameter `Infcx` → `D` in solver code  
- Move `infcx.rs` → `delegate.rs` to reflect actual purpose

## Changes

### Method Rename: `interner()` → `cx()`
- Rename `TypeFolder::interner()` to `TypeFolder::cx()` across all implementations
- Update `FallibleTypeFolder::interner()` to `FallibleTypeFolder::cx()`
- Affects ~100+ call sites across compiler

### Generic Parameter: `Infcx` → `D`
- Rename generic parameter in solver from `Infcx` to `D` (for Delegate)
- Update `EvalCtxt<'_, Infcx>` → `EvalCtxt<'_, D>`
- Update trait bounds like `Infcx: SolverDelegate` → `D: SolverDelegate`

### Module Rename: `infcx` → `delegate`
- Move `rustc_next_trait_solver/src/infcx.rs` → `delegate.rs`
- Update all imports from `crate::infcx::SolverDelegate` → `crate::delegate::SolverDelegate`

## Rationale

- **`cx()` vs `interner()`**: More generic name, "context" better reflects usage pattern
- **`D` vs `Infcx`**: Abstracts away from specific "inference context" to general "delegate" pattern
- **`delegate.rs`**: Module name now matches the `SolverDelegate` trait it contains