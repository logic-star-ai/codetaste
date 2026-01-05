# Refactor: Create `nano::store` library/namespace/directory

## Summary

Restructure storage layer into dedicated `nano::store` library with proper interface/implementation separation and clearer namespace hierarchy.

## Changes

### Namespace Reorganization
- Rename `nano::store` class → `nano::store::component`
- Move LMDB implementation to `nano::store::lmdb::*`
- Move RocksDB implementation to `nano::store::rocksdb::*`

### File Structure
- Relocate files from `nano/node/{lmdb,rocksdb}/` → `nano/store/{lmdb,rocksdb}/`
- Create interface headers in `nano/store/`:
  - `account.hpp`, `block.hpp`, `confirmation_height.hpp`
  - `pending.hpp`, `frontier.hpp`, `online_weight.hpp`
  - `peer.hpp`, `pruned.hpp`, `final.hpp`, `version.hpp`

### Interface Extraction
- Extract abstract interfaces for store components
- Each backend (LMDB/RocksDB) implements these interfaces
- Enables better testability and potential future backends

### Type Consolidation
- Transaction types: `nano::{read,write}_transaction` → `nano::store::{read,write}_transaction`
- Database values: `nano::mdb_val` → `nano::store::lmdb::db_val`, `nano::rocksdb_val` → `nano::store::rocksdb::db_val`
- Iterators: `nano::store_iterator<K,V>` → `nano::store::iterator<K,V>`

### Build System
- Add `nano/store` subdirectory to CMake
- Configure include directories for new library

## Benefits
- Clear separation of storage concerns
- Proper interface/implementation boundaries
- Better organization for future maintenance
- Foundation for potential additional storage backends