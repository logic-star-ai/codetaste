# Title
Remove `ENABLE/ENABLED/DISABLE/DISABLED` macro definitions from Copter

# Summary
Replace all uses of `ENABLED`/`DISABLED` macros with direct `1`/`0` values throughout ArduCopter codebase. Remove macro definitions from `defines.h`.

# Why
- Eliminates unnecessary indirection through symbolic constants
- Standardizes feature flag definitions to use direct numeric values
- Improves code clarity (no need to remember what `ENABLED` means)
- Aligns with C++ best practices for compile-time constants
- Final vehicle type to complete this refactoring across the project

# Changes
- **defines.h**: Remove `ENABLED`/`DISABLED`/`ENABLE`/`DISABLE` macro definitions
- **Feature flags**: All `#define FEATURE ENABLED` → `#define FEATURE 1`
- **Conditionals**: `#if MODE_X == ENABLED` → `#if MODE_X`
- **Config comments**: Update to reflect new values (e.g., `// ... DISABLED` → `// ... 0`)
- **Hardware definitions**: Update SkyViper hwdef.dat files accordingly

# Scope
- ~60+ files modified across ArduCopter/
- All flight mode enable flags (ACRO, AUTO, BRAKE, CIRCLE, ...)
- Feature flags (AUTOTUNE, TOY_MODE, WEATHERVANE, ...)
- Configuration files (APM_Config.h, config.h, Parameters.*)
- No functional/binary changes except SkyViper variants (-8 bytes on two boards)