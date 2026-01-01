# Rename `SemanticModel::is_builtin` to `SemanticModel::has_builtin_binding`

## Summary
Rename `SemanticModel::is_builtin()` method to `SemanticModel::has_builtin_binding()` for improved clarity and consistency with related methods.

## Why
The current name `is_builtin()` is ambiguous and doesn't clearly communicate what it checks:
- `is_builtin()` returns `true` if a **symbol** has a builtin binding in the current scope (i.e., bound via Python's pre-populated builtins scope)
- This is **distinct** from `resolve_builtin_symbol()` and `match_builtin_expr()` which check whether an AST **node** refers to a symbol from the `builtins` module
- The name doesn't distinguish between checking "symbol bindings" vs "AST node references"

## Changes
- Rename method: `is_builtin()` → `has_builtin_binding()`
- Update all call sites across linter rules to use new name
- Update method documentation to clarify the distinction

## Locations
- Method definition: `crates/ruff_python_semantic/src/model.rs`
- Call sites in rules: `flake8_*`, `pycodestyle`, `pyflakes`, `pylint`, `pyupgrade`, `refurb`, `ruff`, `tryceratops`, ...
- Checker/importer modules