# Title
Move function helpers, date helpers, and signals to core

# Summary
Extract utility modules for signals, date helpers, and function helpers into the core directory structure as part of core extraction effort.

# Why
- Establish clear boundaries between core utilities and higher-level utils
- Improve modularity and organization of foundational utilities
- Group related functionality: data structures, type helpers, etc.

# What Changed
- **Signals**: `src/utils/signals` → `src/core/data-structures/signals`
- **Date helpers**: `src/utils/date` → `src/core/types/date` (parseDate, getDate)
- **Function helpers**: `src/utils/function` → `src/core/types/function` (once)
- **Rate-limit helpers**: `src/utils/rate-limit` → `src/core/types/function` (throttle, debounce)
- Updated ~80+ import statements across extensions/..., src/..., ads/..., 3p/...
- Updated dep-check config allowlists
- Updated forbidden-terms config for `.getTime` allowlist
- Added `Timestamp` typedef for date helper types
- Moved test files to match new structure

# Impact
- No behavioral changes
- All imports updated to use new paths
- Cleaner core organization for foundational utilities