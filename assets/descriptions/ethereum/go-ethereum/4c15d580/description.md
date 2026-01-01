# Title
Refactor: Remove trie → triedb dependency via interface abstraction

## Summary
Inverts the dependency between `trie` and `triedb` packages by introducing interface abstractions, moving database implementations to top-level `triedb/` package, and making trie operations depend on interfaces rather than concrete database types.

## Why
- Eliminates circular dependency concerns between trie and database layers
- Improves package organization and separation of concerns
- Enables better testability through interface-based design

## Changes

### Package Restructuring
- Move `trie/triedb/hashdb/` → `triedb/hashdb/`
- Move `trie/triedb/pathdb/` → `triedb/pathdb/`  
- Move `trie/preimages.go` → `triedb/preimages.go`
- Move `trie.Database` → `triedb.Database`
- Move `trie.Config` → `triedb.Config`

### Interface Abstraction
- Create `triedb/database/database.go` with:
  - `Reader` interface for trie node access
  - `PreimageStore` interface for preimage operations
  - `Database` interface combining both
- Update `trie` package to depend on `triedb/database` interfaces
- Modify `StateTrie` to accept `database.Database` interface

### Code Updates
- Update all imports: `trie.Database` → `triedb.Database`, `trie.Config` → `triedb.Config`
- Rename `mptResolver` → `MerkleResolver` (export for use in triedb)
- Update test implementations to use interface-based approach
- Refactor ~50+ files across `cmd/`, `core/`, `eth/`, `tests/`, etc.

### API Changes
- `trie.NewDatabase()` → `triedb.NewDatabase()`
- `trie.HashDefaults` → `triedb.HashDefaults`
- `state.NewDatabaseWithConfig()` now accepts `*triedb.Config`
- All trie constructors now accept `database.Database` interface