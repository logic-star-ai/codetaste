Title
-----
Refactor: Streamline util library to reduce kernel dependencies

Summary
-------
Reorganize utility functions and types to remove non-essential functionality from `libbitcoin_util`, which is a dependency of the kernel library.

Why
---
The util library is distributed with the kernel and shouldn't contain higher-level code targeted at node/wallet/GUI that external kernel applications shouldn't call. This improves code organization and makes the kernel's dependency surface clearer.

What Changed
------------
**Moved to common/:**
- `util/fees.h` + `util/error.h` → `common/messages.h` (user-facing message generation functions)
- `util/message.*` → `common/signmessage.*` (message signing functionality)
- `chainparamsbase` from util to common

**Moved to crypto/:**
- `HexStr()` and `HexDigit()` → `crypto/hex_base.h`
- `memory_cleanse` from util to crypto

**Moved to script/:**
- Remaining `util/spanparsing.h` functions → `script/parsing.h` (descriptor/miniscript parsing)

**String utilities reorganization:**
- `Split()` functions moved from `spanparsing.h` to `util/string.h` within `util` namespace
- String functions in `util/string.h` now properly namespaced

**Type reorganization:**
- `TransactionError` enum → `node/types.h`
- New `PSBTError` enum → `common/types.h`

**Documentation & tooling:**
- Added `check-deps.sh` script to verify library dependencies
- Updated `doc/design/libraries.md` to clarify util vs common distinction

Impact
------
- Files removed: `util/fees.h`, `util/error.h`, `util/spanparsing.h`
- Namespace changes require `using` declarations across codebase
- No functional changes, pure refactoring