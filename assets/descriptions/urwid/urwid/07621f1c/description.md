# Title
Migrate codebase to Python 3.7+ only (drop Python 2 support)

# Summary
Complete migration of urwid to Python 3.7+ by removing all Python 2 compatibility code and modernizing syntax. This includes removing the compatibility layer, updating string/bytes handling, modernizing class definitions, and using Python 3+ idioms throughout.

# Changes Overview

## Compatibility Layer Removal
- Remove `urwid.compat` helpers: `ord2`, `bytes3`, `text_type`, `xrange`, `text_types`, `B`, `with_metaclass`, `chr2`
- Remove `widget.update_wrapper` (Python 2 backport of `functools.update_wrapper`)
- Remove `split_repr.python3_repr` utility

## Syntax Modernization
- Add `from __future__ import annotations` to all modules
- Remove `u` prefix from string literals
- Replace `bytes()` with `b''` literals
- Change `== None` → `is None`, `!= None` → `is not None`
- Remove explicit `object` subclassing
- Convert `super(ClassName, self)` → `super()`
- Replace `set([...])` with `{...}` set literals
- Convert string formatting to f-strings where appropriate
- Remove Python 2 specific methods (`__delslice__`, `__setslice__`)

## Exception Handling
- Replace `IOError`, `select.error`, `socket.error` with unified `OSError`

## Class/Property Updates
- Use native `@classmethod` and `@property` decorators
- Replace custom `self.__super` pattern with `super()` calls
- Convert property lambdas to explicit `@property` methods where clarity improves

## Build/CI Updates
- Update `tox.ini` to test Python 3.7-3.11 only
- Update `.travis.yml` to run Python 3.7+ tests
- Update `setup.py` classifiers and remove Python 2 compatibility checks
- Automatically sort imports throughout codebase

## Deprecation Warnings
- Add `DeprecationWarning` to deprecated methods (e.g., `run_wrapper`, `emit_signal` with `user_arg`)
- Add warnings for `FlowWidget`, `BoxWidget`, `FixedWidget` base classes

## Documentation/Examples
- Update URLs from `http://excess.org/urwid/` → `https://urwid.org/`
- Fix `docs/manual/wcur2.py` to be valid Python code
- Update all examples to use Python 3 syntax

# Why
- Python 2 reached EOL on January 1, 2020
- Simplifies codebase by removing ~500 lines of compatibility code
- Enables use of modern Python features and idioms
- Reduces maintenance burden
- Aligns with ecosystem-wide Python 3 migration