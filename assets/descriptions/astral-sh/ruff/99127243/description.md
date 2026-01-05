# Remove parser dependency from `ruff-python-ast`

## Summary

Break circular dependency between `ruff-python-ast` and `rustpython-parser` by extracting and reorganizing code into new crates. This is a pure refactoring with no logical changes - only code movement between crates.

## Why

Preparation for merging `rustpython-ast` and `ruff_python_ast`. The merger requires `ruff_python_ast` to have no dependency on `rustpython-parser` (since parser depends on AST).

## Changes

### Crate Renaming
- `ruff_rustpython` → `ruff_python_parser`

### Crate Merging
- `ruff_textwrap` → merged into `ruff_python_trivia` (uses `PythonWhitespace`)

### New Crates Created

**`ruff_source_file`**
- Contains: `SourceFile`, `Locator`, `SourcePosition`, `LineIndex`
- Non-Python-specific source code utilities

**`ruff_python_codegen`**  
- Contains: `Stylist`, `Generator`, `round_trip()`
- Python code generation utilities

**`ruff_python_index`**
- Contains: `Indexer`, `CommentRanges`, `CommentRangesBuilder`
- AST indexing and comment handling

## Scope

- [x] Extract source file handling to `ruff_source_file`
- [x] Extract codegen utilities to `ruff_python_codegen`  
- [x] Extract indexing to `ruff_python_index`
- [x] Update ~200+ import statements across codebase
- [x] Update `Cargo.toml` dependencies
- [x] Ensure `ruff_python_ast` no longer depends on `rustpython-parser`