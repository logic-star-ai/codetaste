# Title
-----
Adopt existing namespaces into OpenRCT2 namespace hierarchy

# Summary
-------
Restructure existing namespaces to nest under `OpenRCT2::` root namespace. Add temporary `using namespace OpenRCT2` statements to compilation units to maintain compilation during this transitional refactoring phase.

# Why
---
- Legacy namespaces originated when most codebase was C, not C++
- Need proper C++ namespace hierarchy with `OpenRCT2` at root
- Foundation for eventual namespace tree following folder structure

# Changes
---------
**Namespace relocations:**
- `Dropdown` → `OpenRCT2::Dropdown`
- `Graph` → `OpenRCT2::Graph`
- `LandTool` → `OpenRCT2::LandTool`
- `ThemeManager` → `OpenRCT2::ThemeManager`
- `Editor` → `OpenRCT2::Editor`
- `ParkImporter` → `OpenRCT2::ParkImporter`
- `TrackImporter` → `OpenRCT2::TrackImporter`
- `GameActions` → `OpenRCT2::GameActions`
- `RCT1`, `RCT2`, `RCT12::*` → `OpenRCT2::RCT1`, `OpenRCT2::RCT2`, `OpenRCT2::RCT12::*`
- `TrackElemType` → `OpenRCT2::TrackElemType`
- Various utility namespaces (`Console`, `File`, `Collections`, `Crypt`, etc.)

**Moved into OpenRCT2 namespace:**
- `RideConstructNew()` and `BuildSpecialElementsList()` functions
- `RideConstructionState` enum
- Track/ride construction related constants and data structures

**Temporary compatibility layer:**
- Added `using namespace OpenRCT2` to ~200+ compilation units
- Allows gradual migration until units placed in proper namespaces

# Scope
------
- UI layer (`openrct2-ui/`)
- Core engine (`openrct2/`)
- Actions system
- Ride/track systems
- RCT1/RCT2 compatibility layers
- Test files

# Implementation Notes
---------------------
- Fully qualified names used where `using` statement inappropriate
- Title sequence manager functions consolidated into namespace
- TitleSequenceManager functions moved from global to `OpenRCT2::TitleSequenceManager::`
- Constants like `PREDEFINED_INDEX_CUSTOM` → `kPredefinedIndexCustom` moved to namespace

# Next Steps
-----------
_(Not in scope for this commit - future work)_
- Remove temporary `using` statements
- Place compilation units in appropriate namespaces
- Build full namespace tree following folder structure