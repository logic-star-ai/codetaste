# Remove "z64" prefix from all header files

## Summary
Remove the `z64` prefix from all header files and update all `#include` statements throughout the codebase to use the new names.

## Changes
- Rename all `include/z64*.h` → `include/*.h` (remove z64 prefix)
- Update include guards accordingly (e.g., `Z64ACTOR_H` → `ACTOR_H`)
- Update all `#include "z64*.h"` → `#include "*.h"` across...
  - `src/...`
  - `assets/...`
  - `tools/...`

## Special Cases
- `z64play.h` → `play_state.h` (added "state" suffix to match other gamestate headers)
- `z64math.h` → `z_math.h` (retain z_ prefix to distinguish from libc's `math.h`)

## Why
- Simplify header naming convention
- Remove unnecessary prefix that clutters the include structure
- Improve consistency with modern C project conventions