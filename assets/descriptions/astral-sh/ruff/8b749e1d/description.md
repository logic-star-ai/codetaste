# Inconsistent AST Expression Type Naming

## Summary
Remove redundant `Expr` postfix from `ExprNamedExpr`, `ExprIfExpr`, and `ExprGeneratorExpr` types to align with naming conventions used by other expression types in the AST.

## Why
Most expression types follow the pattern `Expr{Name}` (e.g., `ExprYield`, `ExprAwait`, `ExprStringLiteral`), but three types have an extra `Expr` suffix: `ExprNamedExpr`, `ExprIfExpr`, and `ExprGeneratorExpr`. While this may align with Python's AST naming, it creates unnecessary inconsistency and verbosity in the codebase.

## Changes
Rename expression types for consistency:
- `ExprNamedExpr` → `ExprNamed`
- `ExprIfExpr` → `ExprIf`  
- `ExprGeneratorExpr` → `ExprGenerator`

Update corresponding enum variants:
- `Expr::NamedExpr` → `Expr::Named`
- `Expr::IfExp` → `Expr::If`
- `Expr::GeneratorExp` → `Expr::Generator`

## Scope
Update all references across:
- AST node definitions
- Visitors and transformers
- Pattern matching
- Formatters and code generation
- Linter rules and semantic analysis
- Helper methods (`is_*`, `as_*`)