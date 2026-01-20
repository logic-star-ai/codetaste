# Reorganize option header files

Restructure option-related headers to better separate concerns:
- Move `vimoption_T` struct → `option.h`
- `option_defs.h` → option-related types only (`OptVal`, `OptValType`, `optset_T`, ...)
- Create `option_vars.h` → global option variables (replaces Vim's `option.h`)
- Remove mutual inclusion between `option_defs.h` and `option_vars.h`