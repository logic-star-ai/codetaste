# Refactor: Reorganize and simplify `testutil/` module structure

## Summary

Flatten and simplify the `testutil/` directory structure by removing nested subdirectories, consolidating utilities, and inlining rarely-used helpers. This reduces the surface area of the `pantsbuild.pants.testutil` distribution.

## Changes

### Module relocations
- `testutil.engine.util` → `testutil.engine_util`
- `testutil.option.util` → `testutil.option_util`
- `interpreter_selection_utils.py` → `python_interpreter_selection.py`
- `process_handler.py` → `_process_handler.py` (mark as private)

### Function moves
- `create_subsystem()` and `create_goal_subsystem()` from `engine_util` → `option_util`

### Inlined/deleted utilities
- Inline `pexrc_util.py` → `python_setup_test.py`
- Inline `git_util.py` → `changed_integration_test.py`
- Inline `retry.py` → `pantsd_integration_test_base.py`
- Inline `option/fakes.py` → `options_test.py`
- Delete `process_test_util.py` (unused)

### Simplified `engine_util.py`
- Inline `fmt_rule()` into `rules_test.py`
- Remove `init_native()` (use `Native()` directly)
- Remove nested `engine/` and `option/` subdirectories

## Why

- Reduce public API surface committed to maintaining in testutil distribution
- Eliminate rarely-used utilities from 2.0 codebase (e.g., `testutil.option.fakes`)
- Flatten directory structure for simpler navigation
- Clarify what's intended for plugin authors vs internal use