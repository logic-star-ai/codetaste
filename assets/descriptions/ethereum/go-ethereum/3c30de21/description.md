# Title

Move genesis alloc types from `core` to `core/types`

# Summary

Relocate `GenesisAccount` and `GenesisAlloc` types from the `core` package to `core/types` to make them accessible for public-facing APIs.

# Why

These types belong in `core/types` rather than `core` because:
- They are fundamental data structures needed in public user-facing APIs
- The `core` package should contain internal blockchain logic, not public API types
- Better package organization and separation of concerns

# Changes

**New file: `core/types/account.go`**
- `Account` type (renamed from `GenesisAccount`): represents account state with code, storage, balance, nonce, privateKey
- `GenesisAlloc` type: map of addresses to accounts for genesis block allocation
- Helper types: `storageJSON` for JSON marshaling/unmarshaling
- Generated code moved from `core/gen_genesis_account.go` → `core/types/gen_account.go`

**Updated: `core/genesis.go`**
- Added backwards-compatible type aliases:
  - `type GenesisAccount = types.Account`
  - `type GenesisAlloc = types.GenesisAlloc`
- Changed `Genesis.Alloc` field type from `GenesisAlloc` → `types.GenesisAlloc`
- Refactored methods: `(GenesisAlloc).hash()` → `hashAlloc()`, `(GenesisAlloc).flush()` → `flushAlloc()`

**Updated imports across codebase:**
- `core.GenesisAccount` → `types.Account`
- `core.GenesisAlloc` → `types.GenesisAlloc`
- Updated in: test files, API implementations, simulated backends, tracers, cmd tools, etc.

# Compatibility

Fully backwards compatible via type aliases in `core` package.