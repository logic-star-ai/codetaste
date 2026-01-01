Title
-----
Migrate calls from alias file to appropriate store/types

Summary
-------
Remove the `types/store.go` alias file and migrate all references to use `store/types` directly. This involves updating imports, type references, and function signatures throughout the codebase to reference store types from their actual location rather than through SDK type aliases.

Why
---
- **Reduce indirection**: Aliases in `types/store.go` create unnecessary indirection making it harder to understand type origins
- **Improve code clarity**: Direct imports make it clearer where types are actually defined
- **Better package organization**: Store-related types should be referenced from the store package
- **Simplify codebase**: Remove an entire abstraction layer that serves little purpose

Changes Required
----------------
- Remove `types/store.go` and `types/store_internal_test.go`
- Add `storetypes "github.com/cosmos/cosmos-sdk/store/types"` imports throughout codebase
- Replace SDK type aliases with direct store type references:
  - `sdk.KVStore` → `storetypes.KVStore`
  - `sdk.Iterator` → `storetypes.Iterator`
  - `sdk.GasMeter` → `storetypes.GasMeter`
  - `sdk.MultiStore` → `storetypes.MultiStore`
  - `sdk.CommitMultiStore` → `storetypes.CommitMultiStore`
  - `sdk.StoreDecoderRegistry` → `storetypes.StoreDecoderRegistry`
  - ... (and similar for other store types)
- Update function calls:
  - `sdk.NewInfiniteGasMeter()` → `storetypes.NewInfiniteGasMeter()`
  - `sdk.NewGasMeter()` → `storetypes.NewGasMeter()`
  - `sdk.NewKVStoreKey()` → `storetypes.NewKVStoreKey()`
  - `sdk.KVStorePrefixIterator()` → `storetypes.KVStorePrefixIterator()`
  - ... (etc.)
- Move helper functions (`NewTransientStoreKeys`, `NewMemoryStoreKeys`, `StoreDecoderRegistry`) to `store/types/store.go`
- Update `UPGRADING.md` to document the migration

Files Affected
--------------
- `types/store.go` (delete)
- `types/store_test.go` (delete)  
- `types/store_internal_test.go` (delete)
- `store/types/store.go` (add helper functions)
- `baseapp/*`
- `x/*/keeper/*` (all modules)
- `x/*/migrations/*`
- Test files across the codebase
- ... (100+ files)