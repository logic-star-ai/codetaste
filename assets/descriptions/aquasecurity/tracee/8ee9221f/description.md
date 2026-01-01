# Refactor: Reorganize `common/` module structure into focused packages

## Summary

Reorganize files directly under `common/` root into logical, specific packages to improve code organization and discoverability. Split monolithic utility files into focused packages with clear responsibilities and move specialized functionality to appropriate locations.

## Changes

**New Packages Created:**
- `common/bitwise/` - Bit manipulation utilities (`HasBit`, `ClearBit`, `SetBit`, etc.)
- `common/hash/` - Murmur hash functions for task IDs and data structures
- `common/interfaces/` - Generic interfaces (`Cloner[T]`, `Iterator[T]`)
- `common/stringutil/` - String manipulation utilities (`ReverseString`, `TrimTrailingNUL`)

**Package Moves:**
- `common/environment/kernel_symbols` → `pkg/symbols/` (specialized kernel symbol management, not generic utility)
- `common/symbol_table` → `pkg/symbols/table` (co-locate with kernel symbols)

**Package Mergers:**
- Merge `common/read/` into `common/fileutil/` (consolidate file operation utilities including protected memory-mapped file reading)

**Removed Files:**
- `common/common.go` - split into specific packages
- `common/numbers.go` - functions moved to appropriate packages (`timeutil`)

**Import Updates:**
- Update all imports across codebase:
  - `common.HasBit` → `bitwise.HasBit`
  - `common.HashTaskID` → `hash.HashTaskID`
  - `common.Cloner` → `interfaces.Cloner`
  - `common.TrimTrailingNUL` → `stringutil.TrimTrailingNUL`
  - `environment.KernelSymbolTable` → `symbols.KernelSymbolTable`
  - `read.NewProtectedReader` → `fileutil.NewProtectedReader`

**Documentation:**
- Update `common/README.md` with new package descriptions
- Consolidate fileutil information

## Why

- **Better separation of concerns** - Avoid monolithic utility files with unrelated functions
- **Improved discoverability** - Clear package names indicate purpose without reading documentation
- **Focused packages** - Each package has single, well-defined responsibility
- **Cleaner dependencies** - More granular imports reduce unnecessary coupling
- **Avoid "utils" anti-pattern** - Replace generic utils with specific, named packages

## Testing

- [ ] All existing tests pass with updated imports
- [ ] No behavioral changes to public APIs
- [ ] Build succeeds across all packages