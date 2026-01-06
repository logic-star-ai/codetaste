# Consolidate Extension Modules into `pandas/_libs`

Reorganize Cython/C extension modules by moving them from scattered locations (`pandas/`, `pandas/src/`) into a centralized `pandas/_libs/` directory. This makes the import structure more uniform and cleans up the top-level namespace.