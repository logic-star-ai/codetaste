# Move `stable_mir` back to its own crate

## Summary
Move `stable_mir` implementation from `rustc_smir` back to the `stable_mir` crate, completing the refactoring to break circular dependencies between crates.

## Why
- Complete the refactoring started in PR #139319
- Resolve circular dependency between `rustc_smir` and `stable_mir` crates
- Establish clearer separation: `rustc_smir` contains rustc-side implementation, `stable_mir` contains the public stable API
- Improve crate architecture and maintainability

## Changes
- **Move module tree**: `rustc_smir/src/stable_mir/*` → `stable_mir/src/*`
- **Flatten rustc_smir**: `rustc_smir/src/rustc_smir/*` → `rustc_smir/src/*` 
- **Move `rustc_internal`**: From `rustc_smir` to `stable_mir` crate
- **Update dependencies**: Add rustc crate dependencies to `stable_mir/Cargo.toml` (rustc_abi, rustc_hir, rustc_middle, rustc_session, rustc_span, rustc_target, scoped-tls, serde, tracing)
- **Add deprecation notice**: Leave empty deprecated `rustc_internal` module in `rustc_smir` to guide users to `stable_mir::rustc_internal`
- **Update imports**: Change all references from `rustc_smir::stable_mir::*` to `stable_mir::*` throughout tests and internal code
- **Update import patterns**: Remove `#[macro_use] extern crate rustc_smir;`, add `#[macro_use] extern crate stable_mir;` where needed