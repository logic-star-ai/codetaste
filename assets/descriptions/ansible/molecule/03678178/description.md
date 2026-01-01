# Collapse utils module into single util.py file

## Summary
Consolidate the `molecule.utils.*` module structure by moving all utility functions into a single `molecule.util` module at the package root.

## Why
- Simplify module organization (flat is better than nested)
- Resolve circular import issues between utils submodules
- Reduce import path complexity (`molecule.util` vs `molecule.utils.util`)

## Changes
- Move `src/molecule/utils/util.py` → `src/molecule/util.py`
- Consolidate `to_bool()` from `boolean.py` into main `util.py`
- Update all imports: `molecule.utils.util` → `molecule.util`
- Update all imports: `molecule.utils.boolean` → `molecule.util`
- Remove `src/molecule/utils/` directory and files (`__init__.py`, `boolean.py`, `utils/util.py`)

## Scope
- ~40 files updated with import path changes
- All existing functionality preserved
- Tests updated accordingly
- No behavioral changes