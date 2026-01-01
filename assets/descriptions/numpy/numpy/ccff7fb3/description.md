# Reorganize non-constant global statics into structs

## Summary

Refactor scattered mutable and immutable static global variables throughout the NumPy C codebase into organized structs exposed via `multiarraymodule.h`.

## Why

- Global statics are currently scattered throughout the codebase, making state management difficult to track and reason about
- Current organization makes thread-safety issues hard to identify and fix
- Consolidating globals into structs prepares for future thread-safety improvements

## What Changed

Created four new structs to organize different categories of global state:

- **`npy_interned_str`**: Interned string constants (e.g., `__array__`, `__array_ufunc__`, `dtype`, `where`, ...)
- **`npy_static_pydata`**: Immutable PyObjects initialized during module init (e.g., exception classes, cached function references, default values, ...)
- **`npy_static_cdata`**: Immutable C data initialized during module init (e.g., lookup tables, `sys.flags.optimize` value, ...)
- **`npy_thread_unsafe_state`**: State stored in thread-unsafe manner (e.g., lazily-initialized cached imports, mutable flags, ...)

## Implementation

- Added `numpy/_core/src/multiarray/npy_static_data.c` and `.h` to define and initialize the structs
- Moved ~100+ scattered `static PyObject*` and other globals into appropriate struct
- Updated all references throughout `multiarray/` and `umath/` modules to use new struct members
- Consolidated initialization logic into `initialize_static_globals()` and related functions
- Added verification that all struct members are initialized before module load completes

## Follow-up

Items in `npy_thread_unsafe_state` need to be refactored for thread-safety in future PRs.