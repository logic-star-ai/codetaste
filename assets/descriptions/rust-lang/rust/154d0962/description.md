# Rename `hir::Local` to `hir::LetStmt` for clarity

## Summary
Rename `hir::Local` struct to `hir::LetStmt` throughout the codebase to more accurately represent its purpose as a let statement/binding representation.

## Why
The name `Local` is ambiguous - it could refer to local variables in general, but this struct specifically represents `let` statement bindings in the HIR. `LetStmt` makes the purpose more explicit and reduces confusion.

## Changes
- Rename `struct Local` → `struct LetStmt` in `rustc_hir`
- Update `StmtKind::Let(&'hir Local<'hir>)` → `StmtKind::Let(&'hir LetStmt<'hir>)`
- Rename `Node::Local` → `Node::LetStmt`
- Rename `expect_local()` → `expect_let_stmt()`
- Update all references across compiler and clippy

## Scope
- Keep `visit_local()` method name unchanged
- Keep `LocalSource` enum unchanged
- Focus on the struct and node type renaming only