# Title

Split typechecking logic into separate `typecheck` package

# Summary

Refactor compiler to extract all typechecking logic from `gc` package into new `cmd/compile/internal/typecheck` package for better code organization and modularity.

# Why

- `gc` package has grown too large and monolithic
- Mixing typechecking with code generation makes codebase harder to navigate and maintain
- Clear separation of concerns improves maintainability

# Changes

## Package Structure
- Create new `cmd/compile/internal/typecheck` package
- Move files: `builtin.go`, `const.go`, `dcl.go`, `func.go`, `iexport.go`, `iimport.go`, `typecheck.go`, `universe.go`, `stmt.go`, `subr.go`, `syms.go`, etc.

## API Renaming
- `typecheck(n, ctxExpr)` → `Expr(n)` / `Stmt(n)` / `AssignExpr(n)` etc.
- `typecheckslice(ns, ctx)` → `Exprs(ns)` / `Stmts(ns)`
- Internal `typecheck` → `check`
- Dozens of other functions: `adddot` → `AddImplicitDots`, `expandmeth` → `CalcMethods`, `checkreturn` → `CheckReturn`, etc.

## Exported Variables/State
- `Target` → `typecheck.Target`
- `dclcontext` → `typecheck.DeclContext`
- `typecheckok` → `typecheck.TypecheckAllowed`
- `dotImportRefs` → `typecheck.DotImportRefs`
- `declImporter` → `typecheck.DeclImporter`

## Import/Export Handling
- Move binary import/export into typecheck package
- Keep exporter logic separate in `export.go`

## Function Organization
- Closure handling: `ClosureType`, `PartialCallType`, `CaptureVars`
- Declaration helpers: `DeclFunc`, `DeclVars`, `Declare`, etc.
- Type construction: `NewFuncType`, `NewStructType`, `NewMethodType`
- Utilities: `Lookup`, `LookupNum`, `AutoLabel`, `Temp`, `TempAt`, etc.

# Scope

All `gc` package files updated to import and use `typecheck` package. No functional changes, pure refactoring.