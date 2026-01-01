# Refactor: rename "Dictionary" => "Dict"

## Summary

Rename all occurrences of "Dictionary" to "Dict" throughout the codebase for consistency and brevity. Update API metadata, C types, Lua bindings, documentation, and tests.

## Why

- Long overdue TODO item
- Shorter, more concise naming convention
- Aligns with existing patterns (e.g., "Array" not "ArrayType")
- **Not a breaking change**: clients don't actually use the `return_type` or parameter type names from `api_info()` (evidence: `ArrayOf(Integer, 2)` didn't break any clients when added)

## Scope

### C API
- Rename `kObjectTypeDictionary` → `kObjectTypeDict`
- Update `Dictionary` typedef → `Dict`
- Rename `nvim__id_dictionary()` → `nvim__id_dict()`
- Update all API function signatures using `Dictionary` → `Dict`
- Update API metadata generation

### Lua bindings
- Update `vim.api.nvim__id_dictionary` → `vim.api.nvim__id_dict`
- Update all wrapper functions using "Dictionary" → "Dict"

### Documentation
- Update `runtime/doc/api.txt`, `runtime/doc/lsp.txt`, etc.
- Replace "Dictionary" → "Dict" in docstrings
- Update terminology in help text

### Tests
- Update test expectations for API function names
- Update assertions checking for "Dictionary" → "Dict"

### Generators
- Update `gen_api_dispatch.lua`, `gen_eval_files.lua`, etc.
- Replace `DictionaryOf()` → `DictOf()`
- Update metadata output

## Implementation notes

- Keep `VAR_DICT` type unchanged (internal VimL representation)
- No functional changes, purely terminology
- ... update all references consistently across the codebase
- ... ensure generators produce correct metadata