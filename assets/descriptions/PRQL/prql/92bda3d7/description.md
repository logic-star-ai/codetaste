# Rename `prql_compiler::ast` to `prql_compiler::ir`

## Summary
Rename the `ast` module in `prql_compiler` to `ir` (intermediate representation) to better reflect its purpose now that a dedicated `prql_ast` crate exists for the actual AST.

## Why
With the introduction of a proper `prql_ast` crate, the structures in `prql_compiler` are no longer the abstract syntax tree but rather intermediate representations used during compilation. The naming should reflect this distinction.

## Changes
- `prql_compiler::ast` → `prql_compiler::ir`
- `prql_compiler::ast::pl` → `prql_compiler::ir::pl`  
- `prql_compiler::ast::rq` → `prql_compiler::ir::rq`
- Module doc: "Abstract Syntax Tree" → "Intermediate Representations of Abstract Syntax Tree"
- Trait rename: `AstFold` → `PlFold`
- All imports updated throughout codebase (`use crate::ast::...` → `use crate::ir::...`)
- File structure: `src/ast/*` → `src/ir/*`

## Module Visibility
Some submodules changed from `pub mod` to non-public (e.g., `fold`, `extra`, `expr`, `stmt`) with selective re-exports via `pub use`, cleaning up the public API surface.