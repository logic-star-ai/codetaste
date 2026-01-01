# Title
-----
Clean up circular imports and establish module import hierarchy

# Summary
-------
Refactor codebase to eliminate circular imports by establishing a clear module import nesting hierarchy and moving/renaming conflicting functions.

# Why
---
Circular imports cause issues with module loading and make the codebase harder to maintain. Need clear dependency structure.

# Changes
---------

**Resolve duplicate function names:**
- Rename `mne._fiff.pick._get_ch_type` → `_get_plot_ch_type` 
- Move to `mne.viz.utils` (plotting-specific)

**Decouple modules:**
- Remove `mne.viz` imports from `mne.channels`
- Nest imports following hierarchy

**Reorganize source_space:**
- Convert `mne/source_space.py` → `mne/source_space/_source_space.py`
- Update all imports throughout codebase

**Establish import hierarchy:**
- Define `IMPORT_NESTING_ORDER` tuple in test file
- Order: `fixes` → `defaults` → `utils` → `_fiff` → ... → `viz` → ... → `preprocessing`
- Modules must nest imports from modules below them in hierarchy
- Add AST-based test to enforce hierarchy

**Nest imports:**
- Move module-level imports to function-level where needed
- Affected: `transforms`, `annotations`, `event`, `epochs`, `evoked`, `io`, `forward`, `bem`, `viz`, etc.

**Test infrastructure:**
- Add `test_import_nesting_hierarchy()` 
- AST-parse all `.py` files to validate import nesting
- Checks for non-relative `mne.*` imports
- Verifies proper nesting based on hierarchy