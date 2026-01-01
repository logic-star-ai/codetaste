# Move event containers from plaso.events to plaso.containers

## Summary
Relocate event-specific container classes from `plaso/events/` to `plaso/containers/` for better architectural organization.

## Why
Event objects are data containers and belong in the containers package alongside other container classes for consistency and improved code organization.

## Changes
- Move `file_system_events.py`, `plist_event.py`, `shell_item_events.py`, `text_events.py`, `time_events.py`, `windows_events.py` from `plaso/events/` → `plaso/containers/`
- Remove `plaso/events/` package entirely
- Update all imports: `plaso.events.*` → `plaso.containers.*` across:
  - Parsers (80+ files)
  - Parser plugins (bencode, olecf, plist, sqlite, winreg, ...)
  - Analysis modules
  - Tests
- Update Sphinx documentation structure
- Update internal module cross-references