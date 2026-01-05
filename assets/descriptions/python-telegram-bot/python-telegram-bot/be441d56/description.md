# Remove `__dict__` from `__slots__` and drop Python 3.6

## Summary

Major refactoring to improve memory efficiency and enforce stricter attribute management by removing `__dict__` from `__slots__` across all PTB classes. Also drops Python 3.6 support, setting minimum version to **3.7+**.

## Changes

### Drop Python 3.6 Support
- Update CI workflows, pre-commit config, and setup.py to require Python 3.7+
- Update README/docs to reflect new minimum version
- Remove Python 3.6 from test matrix and classifiers

### Remove `__dict__` from `__slots__`
- **`TelegramObject`**: Move `_id_attrs` from class variable to instance variable initialized in `__new__`
  - `__slots__ = ('__dict__',)` → `__slots__ = ('_id_attrs',)`
  - Remove custom `__setattr__` that warned about dynamic attributes
  - Add type hints for `_id_attrs` in `TYPE_CHECKING` block

- **All subclasses**: Remove `_id_attrs` from their `__slots__` (inherited from parent now)
  - Bot*, Chat*, File*, Message*, Payment*, Inline*, Passport*, Sticker*, etc.

- **`ext.Bot`, `ext.ExtBot`, `ext.Dispatcher`, `ext.Updater`, `ext.JobQueue`**: Remove custom `__setattr__` methods

- **`ext.BasePersistence`**: Keep `__dict__` in slots (needed for dynamic method replacement in `__new__`)
  - Change `object.__setattr__` → `setattr` for method assignments

- **`ChatAction`, `ParseMode`, `Filters`**: Empty slots, remove `__setattr__`

- **`ext.filters.BaseFilter`, `ext.Handler`**: Remove `__setattr__` overrides, simplify slot definitions

### Remove Deprecation Warning System
- Delete `set_new_attribute_deprecated()` function from `telegram/utils/deprecate.py`
- Remove all calls to this function across codebase
- Users can no longer set arbitrary attributes on PTB objects (except where `__dict__` explicitly kept)

### Test Updates
- Update all `test_slot_behaviour()` tests to no longer expect/check for:
  - `__dict__` presence (except `BasePersistence`, `Dispatcher`, `CallbackContext`)
  - Deprecation warnings when setting custom attributes
- Add `Dict*` helper classes in conftest.py for testing (subclasses with `__dict__`)
- Update `test_slots.py` to use allowlist approach for classes that should have `__dict__`

## Why

- **Memory efficiency**: Removing `__dict__` reduces per-instance memory overhead
- **Performance**: Faster attribute access via `__slots__`
- **Type safety**: Prevents accidental attribute assignment/typos
- **Cleaner codebase**: Remove deprecation warning infrastructure
- **Python 3.6 EOL**: Python 3.6 reached end-of-life, 3.7+ brings improvements (e.g., guaranteed dict ordering, better slots behavior)