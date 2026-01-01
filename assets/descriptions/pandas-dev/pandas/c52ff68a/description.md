# Consolidate Extension Modules into `pandas/_libs`

## Summary

Reorganize Cython/C extension modules by moving them from scattered locations (`pandas/`, `pandas/src/`) into a centralized `pandas/_libs/` directory. This makes the import structure more uniform and cleans up the top-level namespace.

## Why

- Extension code is currently scattered across `pandas/` and `pandas/src/`
- Top-level namespace is cluttered with internal modules (lib, tslib, json, parser, algos, hashtable, etc.)
- Import paths are inconsistent and confusing
- `pandas/_libs/` should hold both extension source and compiled builds (as it's importable)
- `pandas/_libs/src/` becomes an includes directory for low-frequency changing code

## Changes

### Module Relocations

**Core Extensions:**
- `pandas.lib` → `pandas._libs.lib`
- `pandas.tslib` → `pandas._libs.tslib` 
- `pandas.hashtable` → `pandas._libs.hashtable`
- `pandas.algos` → `pandas._libs.algos`
- `pandas.index` → `pandas._libs.index`
- `pandas._join` → `pandas._libs.join`
- `pandas._period` → `pandas._libs.period`
- `pandas._reshape` → `pandas._libs.reshape`

**IO Extensions:**
- `pandas.json` → `pandas.io.json.libjson`
- `pandas.parser` → `pandas.io.libparsers`
- `pandas.msgpack` → `pandas.io.msgpack`
- `pandas.io.sas.saslib` → `pandas.io.sas.libsas`

**Other Extensions:**
- `pandas._window` → `pandas.core.libwindow`
- `pandas._sparse` → `pandas.sparse.libsparse`
- `pandas._hash` → `pandas.tools.libhashing`
- `pandas._testing` → `pandas.util.libtesting`

### Deprecation Warnings

Add `_DeprecatedModule` wrapper for:
- `pandas.lib` → warns to use `pandas._libs.lib`
- `pandas.tslib` → warns to use `pandas._libs.tslib`
- `pandas.json` → warns to use `pandas.io.json.libjson`
- `pandas.parser` → warns to use `pandas.io.libparsers`

### File Moves

- Move `.pyx`/`.pxd` files from `pandas/*.pyx` to `pandas/_libs/*.pyx`
- Move C/header files from `pandas/src/` to `pandas/_libs/src/`
- Update all internal imports throughout codebase (100+ files)
- Update `setup.py` extension definitions
- Update Makefile paths

## Details

- Update imports in ~80 test files
- Update imports in core modules (algorithms, groupby, internals, ops, etc.)
- Update imports in tseries modules
- Update imports in IO modules
- Add new `pandas/_libs/__init__.py` exposing key types
- Create deprecation shim modules (`pandas/lib.py`, `pandas/tslib.py`, etc.)
- Enhance `_DeprecatedModule` helper to support module renames