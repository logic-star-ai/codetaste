Title
-----
Clean up and simplify includes in `src/align/*` files

Summary
-------
Reduce header dependencies in alignment module by using forward declarations and moving includes to implementation files where possible.

Why
---
- Improves compilation times by reducing transitive include chains
- Reduces coupling between alignment module components
- Makes dependencies more explicit and minimal

Changes
-------

**Forward declarations over includes:**
- Replace `#include "chunk.h"` with `class Chunk;` in headers (add.h, assign.h, braced_init_list.h, ...)
- Replace `#include "ChunkStack.h"` with `class ChunkStack;` where appropriate
- Replace `#include "uncrustify_types.h"` with `#include <cstddef>` when only `size_t` is needed

**Move includes to implementation files:**
- Headers declare minimal dependencies via forward declarations
- Implementation files (.cpp) include actual headers needed for function bodies
- E.g., add.cpp now includes "chunk.h" and "ChunkStack.h" that were removed from add.h

**Remove unnecessary includes:**
- Remove unused `#include "align/preprocessor.h"` and `#include "align/stack.h"` from align.cpp
- Remove unused `#include "indent.h"` from init_brace.cpp
- Remove unused `#include <algorithm>` from func_proto.cpp

**Replace broad includes with specific ones:**
- Use `#include "log_levels.h"` instead of full "uncrustify_types.h" in log_al.h and trailing_comments.h

**Cleanup:**
- Remove historical "split from..." comments from file headers
- Add missing `std::` namespace qualifier for `std::deque`