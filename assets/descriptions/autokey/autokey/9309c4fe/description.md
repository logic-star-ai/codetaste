# Split model module into separate files and resolve circular imports

## Summary
Refactor `autokey.model.__init__.py` by splitting it into separate modules for each class, and move `Key` class + constants from `iomediator` to `model` package to break circular dependencies.

## Why
- Monolithic `model.__init__.py` (~1200 lines) difficult to maintain/navigate
- Circular imports between `model` and `iomediator` prevent proper module testing
- Better separation of concerns improves code organization

## Changes

### Model Package Restructuring
- Split into separate modules:
  - `abstract_abbreviation.py` - `AbstractAbbreviation` class
  - `abstract_hotkey.py` - `AbstractHotkey` class  
  - `abstract_window_filter.py` - `AbstractWindowFilter` class
  - `folder.py` - `Folder` class
  - `phrase.py` - `Phrase` + `Expansion` + `SendMode` enum
  - `script.py` - `Script` + `ScriptErrorRecord`
  - `store.py` - `Store` class
  - `helpers.py` - `TriggerMode` enum + utility functions
  - `key.py` - Moved from `iomediator/key.py`
  - `modelTypes.py` - Type aliases

### Breaking Circular Imports
- Moved `Key` class from `autokey.iomediator.key` → `autokey.model.key`
- Moved constants (`KEY_SPLIT_RE`, `MODIFIERS`, `HELD_MODIFIERS`) from `iomediator.constants` → `model.key`

### Import Updates
- Updated imports in:
  - `configmanager/...`
  - `gtkui/...` 
  - `qtui/...`
  - `scripting/...`
  - `interface.py`, `service.py`, `macro.py`, etc.
  - All tests

## Impact
- All imports changed from `from autokey import model` to specific module imports
- Tests updated and passing
- No functional changes to behavior