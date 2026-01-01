# Title

Decouple pure replication state from storage

# Summary

Refactor replication components to separate pure replication concerns from storage-specific implementation. Establishes cleaner architecture where replication state (epoch, role, durability) is independent of storage, with a handler layer coordinating between them.

# Why

- Current coupling makes replication logic tightly bound to storage implementation
- Hard to reason about replication state vs storage-specific replication concerns  
- Difficult to extend or modify replication behavior independently

# Changes

**New replication module**
- Create `src/replication/` CMake target
- Extract core types to `memgraph::replication` namespace:
  - `ReplicationRole`, `ReplicationMode`, `ReplicationEpoch`
  - `ReplicationState`, `ReplicationClientConfig`, `ReplicationServerConfig`
  - Replication status serialization

**Split replication state**
- `ReplicationState` → pure replication state
  - Epoch lifecycle and ID management
  - Role (MAIN/REPLICA) with persistence
  - Durability configuration restoration
- `ReplicationStorageState` → storage-specific state  
  - Replication clients/server lifecycle
  - Transaction streaming to replicas
  - Commit timestamp tracking
  - Delta/operation replication

**Introduce ReplicationHandler**
- Coordinates between `ReplicationState` and `Storage`
- Provides unified API for:
  - Role switching (MAIN ↔ REPLICA)
  - Replica registration/unregistration
  - Replication restoration

**Decouple interpreter calls**
- Query interpreter uses `ReplicationHandler` instead of direct storage calls
- Storage replication checks go through `repl_state_` member

# Implementation Notes

- Storage still owns both state objects (full decoupling deferred)
- Backward compatible with existing replication behavior
- Lays groundwork for multi-storage replication support
- All tests updated to use new handler API