# Refactor: Remove cluster_id field from codebase

## Summary
Remove unused `cluster_id` field throughout the codebase. The field was originally intended to isolate nodes from different clusters (allowing metasrv to be shared among various GreptimeDB clusters), but is not assigned anywhere and is largely ignored, causing confusion.

## Why
- `cluster_id` is not assigned anywhere in the codebase
- The field is largely ignored and serves no practical purpose
- Tenant isolation will not rely on this field
- Its presence causes confusion about cluster management

## Changes
**Key Structures Updated**:
- Remove `cluster_id` from: `NodeInfoKey`, `DatanodeStatKey`, `DatanodeLeaseKey`, `FlownodeLeaseKey`, `InactiveRegionKey`, `RegionIdent`, `Stat`, etc.
- Remove `TableMetadataAllocatorContext` struct (only contained cluster_id)
- Remove `ClusterId` type alias

**Function Signatures**:
- Update signatures across modules (selector, lease, peer lookup, DDL procedures, etc.) to remove cluster_id parameter
- Simplify `MetaClientBuilder::new()` and related client initialization
- Update `PeerAllocator`, `PartitionPeerAllocator` interfaces

**Backward Compatibility**:
- Hardcode cluster_id to `0` in all metadata key prefixes (`__meta_cluster_node_info-0-...`, `__meta_datanode_stat-0-...`, etc.)
- Ensures existing metadata remains accessible during upgrades

**Dependencies**:
- Update `greptime-proto` to version without cluster_id field

**Tests**:
- Update all tests to reflect removal of cluster_id