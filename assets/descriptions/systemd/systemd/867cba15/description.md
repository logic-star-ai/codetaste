# Title
Refactor `missing_*.h` headers to shadow glibc headers in `src/basic/include/`

# Summary
Rename and relocate `missing_*.h` headers to `src/basic/include/` with canonical glibc names, using `#include_next` to transparently provide missing definitions for older glibc versions.

# Why
When developing with recent glibc, `missing_*.h` includes may be unnecessary. However, supporting baseline glibc versions requires these fallback definitions. CIs running new glibc won't catch missing includes, allowing bugs to slip through.

By shadowing glibc headers in `src/basic/include/`, code can always use standard header names (`#include <sched.h>`), automatically pulling in compatibility definitions when needed.

# Changes

**File Relocations:**
- `src/basic/missing_fcntl.h` → `src/basic/include/fcntl.h`
- `src/basic/missing_sched.h` → `src/basic/include/sched.h`
- `src/basic/missing_mman.h` → `src/basic/include/sys/mman.h`
- `src/basic/missing_pidfd.h` → `src/basic/include/sys/pidfd.h`
- `src/basic/missing_random.h` → `src/basic/include/sys/random.h`
- `src/basic/missing_socket.h` → `src/basic/include/sys/socket.h`
- `src/basic/missing_wait.h` → `src/basic/include/sys/wait.h`

**Header Modifications:**
- Replace `#include <xyz.h>` with `#include_next <xyz.h>`
- Remove `#include "forward.h"` dependencies
- Convert `assert_cc()` → `_Static_assert()`

**Source Code Cleanup:**
- Remove `#include "missing_*.h"` statements across ~40 files
- Add explicit `#include <xyz.h>` where previously implicit
- Simplify include lists throughout codebase

# Benefits
- Prevents accidental omission of compatibility headers
- Uniform use of standard header names
- Maintains backward compatibility with older glibc
- Reduces cognitive overhead for contributors