# Title
-----
Remove all functionality deprecated in PyO3 0.23 (except `IntoPy` and `ToPyObject`)

# Summary
-------
Clean up codebase by removing all deprecated APIs from PyO3 0.23. The `IntoPy` and `ToPyObject` traits are kept for separate handling due to complex fallback logic in macros.

# Why
---
- Reduce API surface and maintenance burden
- Eliminate confusion from multiple deprecated aliases/methods
- Prepare codebase for 0.25.0 release

# Scope
-----
Remove deprecated items across all modules:

**Renamed methods** (removed `_bound` suffix):
- `Python::{eval_bound, run_bound, import_bound, get_type_bound}` → `{eval, run, import, get_type}`
- `PyErr::{from_type_bound, from_value_bound, value_bound, traceback_bound, get_type_bound, ...}` → variants without `_bound`
- `PyAny::{iter, is_ellipsis}` → `try_iter` / use `.is(py.Ellipsis())`
- Similar for `Py*` types: `PyString`, `PyBytes`, `PyList`, `PyDict`, `PyTuple`, ...

**Type aliases**:
- `PyLong` → `PyInt`
- `PyUnicode` → `PyString`

**Module items**:
- `class::methods::*` (implementation details)
- `wrap_pyfunction_bound!` → `wrap_pyfunction!`

**Constructors/helpers**:
- `Py*::new_bound()` → `Py*::new()`
- `Py*::from_bound()` → `Py*::from()`
- `marshal::{dumps_bound, loads_bound}` → `{dumps, loads}`
- `PyWeakref::get_object()` → `upgrade()`

**Version bump**:
- All crates: `0.24.0` → `0.25.0-dev`