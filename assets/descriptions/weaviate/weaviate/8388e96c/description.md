# Title
Refactor cluster package for clear RAFT/schema separation

## Summary
Reorganize cluster package structure to establish clear boundaries between RAFT consensus logic, schema management, and supporting utilities. Extract components into dedicated subpackages and improve naming conventions for better maintainability.

## Why
Current cluster implementation has unclear separation of concerns, making code navigation and maintenance difficult. RAFT logic, schema management, and utility code are intermingled, creating cognitive overhead when working with the codebase.

## Changes

### Package Structure
- Extract `bootstrap` → `cluster/bootstrap/`
- Extract `schema` + `schema_reader` → `cluster/schema/`
- Extract resolvers (RAFT/RPC/Node-to-addr) → `cluster/resolver/`
- Create `cluster/types` for shared types/errors
- Move test fakes → `usecases/fakes/` for reusability

### Naming Improvements
- `Service` → `Raft` (clearer intent)
- `retry_schema` → `SchemaReader`
- `version_schema` → `VersionedSchemaReader`
- `ServerName2PortMap` → `NodeNameToPortMap`
- `AddrResolver` → `NodeToAddressResolver`

### File Organization
Split monolithic files:
- `store.go` → `store.go` + `store_apply.go` + `store_cluster_rpc.go` + `store_query.go` + `store_snapshot.go`
- Service endpoints → `raft.go` + `raft_cluster_endpoints.go` + `raft_query_endpoints.go` + `raft_schema_endpoints.go`
- Store/Service tests → separate test files

### Architectural Changes
- Introduce `SchemaManager` to mediate between store and schema
- Embed Store config directly (eliminate duplicate structs)
- Separate schema state management from RAFT operations
- Centralize error definitions in `cluster/types`

### Config Consolidation
- Merge duplicate config structures
- Remove redundant `LogLevel` + `LogJSONFormat` from RAFT config
- Consolidate resolver interfaces

## Scope
This is a **refactoring-only** change with no functional modifications. All existing APIs and behaviors remain unchanged.