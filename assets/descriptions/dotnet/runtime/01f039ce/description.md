Title
-----
Remove remaining CRT PAL wrappers and enable standard headers in CoreCLR build

Summary
-------
Refactor CoreCLR to use standard C/C++ library headers and functions instead of Platform Abstraction Layer (PAL) wrappers, eliminating custom implementations and simplifying the build system.

Why
---
- PAL wrappers add maintenance burden with custom implementations of standard functionality
- `-nostdinc` flag prevents using optimized standard library implementations
- Custom `clr_std/` implementations duplicate standard library functionality
- Direct use of standard headers enables better compiler optimizations

Changes
-------
**Build System**
- Remove `-nostdinc` flag from Unix builds
- Add `NOMINMAX` define on Windows to prevent macro conflicts
- Enable including `<algorithm>`, `<cmath>`, `<type_traits>`, etc.

**PAL Wrapper Removal**
- Remove `PAL_malloc`, `PAL_free`, `PAL_realloc` → use `malloc`, `free`, `realloc` directly
- Remove `PAL_qsort`, `PAL_bsearch` wrappers
- Remove `PAL_rand`, `PAL_srand`, `PAL_time` wrappers
- Remove file I/O wrappers (`PAL_fopen`, etc.)
- Update callsites passing 0 to allocation functions to pass 1 instead
- Change `getenv` on non-Windows to use `PAL_getenv` directly (preserving existing behavior)

**Header Changes**
- Delete custom `clr_std/algorithm`, `clr_std/string`, `clr_std/type_traits`, `clr_std/utility`, `clr_std/vector`
- Add `using std::min; using std::max;` throughout codebase
- Include standard headers: `<algorithm>`, `<cmath>`, `<type_traits>`, `<limits>`, etc.
- Remove `#undef` directives for standard library symbols

**Code Fixes**
- Fix `min`/`max` calls with explicit template parameters or casts
- Replace `isfinite`, `isnan` with `std::isfinite`, `std::isnan`
- Fix NULL arithmetic/conversion warnings from proper NULL definition
- Remove placement new redefinitions (use standard version)
- Update string formatting: `_gcvt_s` → `sprintf_s` with `%.*g` format

**Test Cleanup**
- Remove tests specific to PAL wrappers: `bsearch`, `malloc`, `free`, `qsort`, `rand_srand`, `realloc`, `time`, `exit`, `__iscsym`
- Update remaining tests to use standard functions