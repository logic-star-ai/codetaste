Title
-----
Reorganize option header files

Summary
-------
Restructure option-related headers to better separate concerns:
- Move `vimoption_T` struct → `option.h`
- `option_defs.h` → option-related types only (`OptVal`, `OptValType`, `optset_T`, ...)
- Create `option_vars.h` → global option variables (replaces Vim's `option.h`)
- Remove mutual inclusion between `option_defs.h` and `option_vars.h`

Changes
-------
- New file: `src/nvim/option_vars.h`
- ~100+ files updated to include correct header:
  - `#include "nvim/option_defs.h"` → `#include "nvim/option_vars.h"` (where variables needed)
  - Some files now include both headers explicitly
- Update `vim-patch.sh` to map Vim's `option.h` → Neovim's `option_vars.h`

Why
---
- Separate type definitions from variable declarations
- Reduce header coupling/circular dependencies
- Better align with intended separation of concerns
- Clearer distinction: types vs. variables vs. API

Details
-------
**option.h**: Core option API + `vimoption_T` definition  
**option_defs.h**: Types (`OptVal`, `optset_T`, `opt_did_set_cb_T`, ...)  
**option_vars.h**: Global variables (`p_*`, `BV_*`, `WV_*`, flags, ...)