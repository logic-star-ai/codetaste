# Refactor Event Manager into categorized modules

## Summary
Split monolithic `event_manager.hpp` into separate category-specific files and add comprehensive documentation for all events and requests.

## Why
Current Event Manager implementation suffers from:
- Single giant file containing all event definitions
- ~147/540 files recompiled on any change
- Poor modularity and organization
- Lack of documentation for event parameters and behavior
- Difficult for new contributors to understand event system

## What Changed
**File Organization:**
- Split into 4 categories: GUI, Interaction, Lifecycle, Provider
- Split into 2 types: Events, Requests
- Result: 8 new header files under `hex/api/events/`:
  - `events_*.hpp` (gui, interaction, lifecycle, provider)
  - `requests_*.hpp` (gui, interaction, lifecycle, provider)

**Documentation:**
- Added `@brief` descriptions for all events/requests
- Added `@param` documentation for parameters
- Added extended comments where behavior is complex/non-obvious
- Included FIXME notes for unused/misnamed events

**Code Updates:**
- Removed blanket `event_manager.hpp` imports throughout codebase
- Replaced with specific category imports where needed
- Ensures files only include events they actually use

## Result
- Reduced compilation dependencies
- Better code organization and discoverability
- Improved onboarding for new contributors
- No user-facing changes (pure DX improvement)