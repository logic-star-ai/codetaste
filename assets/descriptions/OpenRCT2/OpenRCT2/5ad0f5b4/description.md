# Title

Refactor screaming enums to modern C++ naming conventions

# Summary

Convert legacy ALL_CAPS enum values and constants to modern C++ style using `enum class` with lowercase/camelCase naming throughout the codebase.

# Why

- Improve code readability and maintainability
- Follow modern C++ best practices
- Reduce naming collisions and improve type safety with `enum class`
- Make codebase more consistent with contemporary C++ standards

# Changes

Multiple enum types refactored:

**Dialog types (Linux UI)**
- `DIALOG_TYPE::{NONE, KDIALOG, ZENITY}` → `DialogType::{none, kdialog, zenity}`

**File operations**
- `FILE_MODE_{OPEN, WRITE, APPEND}` → `FileMode::{open, write, append}` (enum class)
- `FILE_TYPE::{PARK, SAVED_GAME, ...}` → `FileType::{park, savedGame, ...}` (enum class)

**Directory paths**
- `DIRBASE::{RCT1, RCT2, OPENRCT2, USER, ...}` → `DirBase::{rct1, rct2, openrct2, user, ...}` (enum class)
- `DIRBASE_VALUES` → `DirBaseValues`

**Editor input flags**
- `INPUT_FLAG_EDITOR_OBJECT_*` constants → `EditorInputFlag` enum class with `FlagHolder` wrapper
- Updated flag checking from bitwise ops to `.has()` method

**Station objects**
- `STATION_OBJECT_FLAGS::HAS_PRIMARY_COLOUR` → `StationObjectFlags::hasPrimaryColour`
- `IS_TRANSPARENT` → `isTransparent`, etc.

**Constants**
- `INVALID_DIRECTION` → `kInvalidDirection` (k-prefix for consistency)

# Scope

Changes span across:
- UI context & file browsers
- File I/O operations (FileStream, FileIndex, ...)
- Object loading/selection
- Platform environment & paths
- Pathfinding & entity logic
- Paint/rendering code
- Network code
- Import/export systems

All usages updated consistently throughout ~50+ files.