# Remove redundant compat definitions for Python 3 builtins

## Summary
Remove redundant function/class definitions from `pandas.compat` that were maintained for Python 2/3 compatibility but are now unnecessary as pandas only supports Python 3.5+.

## Why
These definitions are no longer needed since pandas dropped Python 2 support. They add unnecessary indirection and maintenance burden. Using builtins directly is clearer and more pythonic.

## Functions to Remove
- `filter` → use builtin
- `map` → use builtin  
- `range` → use builtin
- `zip` → use builtin
- `next` → use builtin
- `FileNotFoundError` → use builtin
- `ResourceWarning` → use builtin

## Changes Required

**In `pandas/compat/__init__.py`:**
- Remove definitions/assignments for the above functions in PY3 and PY2 branches
- Update module docstring to remove references to these functions

**Throughout codebase:**
- Remove imports of these functions from `pandas.compat` 
- Replace `compat.FileNotFoundError` → `FileNotFoundError`
- Replace `compat.next(...)` → `next(...)`
- Remove from import statements: `from pandas.compat import ..., map, range, zip, filter, ...`

**Test updates:**
- Update `tests/test_compat.py` to remove tests for these functions
- Verify all other tests still pass