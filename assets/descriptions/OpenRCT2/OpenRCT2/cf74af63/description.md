# Reduce Scenario.h Header Dependencies and Remove Unnecessary Includes

## Summary
Remove `Scenario.h` include from ~50 compilation units that don't actually need it, and slim down the `Scenario.h` header itself by removing unnecessary transitive dependencies.

## Why
- **Reduce compilation times**: `Scenario.h` was pulling in heavy headers like `EntityList.h`, `Map.h`, `MapAnimation.h`, `Finance.h`, etc.
- **Reduce coupling**: Many files included `Scenario.h` when they didn't use anything from it
- **Cleaner dependencies**: Files should only include what they directly use

## Changes

### Lighten Scenario.h
Remove unnecessary includes from `Scenario.h`:
- `entity/EntityList.h`
- `management/Finance.h` 
- `management/Research.h`
- `object/Object.h`
- `world/Banner.h`
- `world/Climate.h`
- `world/Map.h`
- `world/MapAnimation.h`

Keep only minimal dependencies:
- `core/Money.hpp`
- `core/Random.hpp`
- `core/String.hpp`
- `localisation/StringIdType.h`
- `ride/RideRatings.h`

### Remove Scenario.h includes
Remove `#include "Scenario.h"` / `#include <openrct2/scenario/Scenario.h>` from files that don't need it:
- UI input/interaction files (MouseInput.cpp, Shortcuts.cpp, ViewportInteraction.cpp, ...)
- Window files (Guest.cpp, GuestList.cpp, Park.cpp, Finances.cpp, ...)
- Action files (CheatSetAction.cpp, GameAction.cpp, RideCreateAction.cpp, ...)
- Entity files (Duck.cpp, Fountain.cpp, Guest.cpp, Peep.cpp, Staff.cpp, ...)
- World/Ride files (Map.cpp, Park.cpp, Scenery.cpp, Vehicle.cpp, Ride.cpp, ...)
- Import/export files (S4Importer.cpp, S6Importer.cpp, ParkFile.cpp, ...)
- ~40+ more files...

### Add explicit includes
Where files transitively depended on headers pulled in by `Scenario.h`, add explicit includes:
- `entity/EntityList.h` (multiple files)
- `world/MapAnimation.h` (Context.cpp, GameState.cpp, ...)
- `scenario/Scenario.h` (ScUi.hpp - actually needs it)