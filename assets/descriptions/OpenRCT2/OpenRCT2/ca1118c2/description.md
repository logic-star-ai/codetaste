# Remove Config.h include (and therefore Drawing.h) from many places

## Summary
Remove unnecessary `Config.h` includes from 36+ compilation units and key headers (`UiContext.h`, `Platform.h`). Extract config enum types into separate `ConfigTypes.h` header for use in header files. Extract currency enums into `CurrencyTypes.h`. Replace `Drawing.h` include in `Config.h` with forward declaration of `Gx` struct.

## Why
- Many files included `Config.h` unnecessarily, only needing forward declarations/enum types
- `Config.h` was pulling in `Drawing.h` (hefty header) just for `Gx` struct definition
- This created cascading dependencies and bloated compile times
- Headers like `UiContext.h` and `Platform.h` only needed config types, not full definitions

## Changes
**New files:**
- `config/ConfigTypes.h` - enum definitions for `Sort`, `TemperatureUnit`, `ScaleQuality`, `MeasurementFormat`, `TitleMusicKind`, etc.
- `localisation/CurrencyTypes.h` - `CurrencyType` and `CurrencyAffix` enums

**Config.h:**
- Include `ConfigTypes.h` and `CurrencyTypes.h` instead of defining enums inline
- Replace `#include "Drawing.h"` with `struct Gx;` forward declaration
- Remove enum definitions (moved to ConfigTypes.h)

**Headers updated to use ConfigTypes.h:**
- `ui/UiContext.h`
- `platform/Platform.h`
- `command_line/SimulateCommands.cpp`
- `interface/StdInOutConsole.cpp`

**Config.h include removed from:**
- Window files: `Cheats.cpp`, `Finances.cpp`, `GuestList.cpp`, `RideList.cpp`, `TextInput.cpp`, `Themes.cpp`, `TitleExit.cpp`, `TitleMenu.cpp`, `TitleOptions.cpp`
- Core files: `Cheats.cpp`, `ParkSetNameAction.cpp`, `NewDrawing.cpp`, `Staff.cpp`, `ObjectRepository.cpp`, `Map.cpp`, `Park.cpp`, ...
- Ride files: `Paint.SmallScenery.cpp`, `MiniGolf.cpp`, `LaunchedFreefall.cpp`, `SplashBoats.cpp`
- Track design: `TrackDesignRepository.cpp`, `TrackDesignSave.cpp`
- Importers: `S6Importer.cpp`, `T6Importer.cpp`
- UI: `DummyUiContext.cpp`
- Tests: `S6ImportExportTests.cpp`

**Explicit includes added where needed:**
- `Currency.h` → `CustomCurrency.cpp`, `Formatting.cpp`, `Localisation.cpp`, `Paint.cpp`, `Platform.Common.cpp`
- `Font.h` → `CommandLine.cpp`, `TTF.cpp`
- `Util.h` → `PlatformEnvironment.cpp`, `TTF.cpp`
- `Drawing.h` retained where actually used

**Platform.h:**
- Add `TTFFontDescriptor` forward declaration
- Include `String.hpp` explicitly (was transitive through Config.h)