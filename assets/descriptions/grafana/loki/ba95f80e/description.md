# Restructure compactor package hierarchy

## Summary
Move compactor package from deeply nested storage path (`pkg/storage/stores/shipper/indexshipper/compactor`) to top-level `pkg/compactor`, aligning with other high-level components (querier, distributor, ruler...).

## Why
Compactor is a core component, not storage implementation detail. Current nesting implies it's storage-specific when it's actually a standalone service.

## Changes
- `pkg/storage/.../compactor/*` → `pkg/compactor/*`
  - Main compactor logic
  - Client (gRPC/HTTP)
  - Deletion management
  - Retention policies
  - Generation numbers
  - Deletion mode
- Store-specific table compaction code remains in store packages:
  - `pkg/storage/.../boltdb/compactor/table_compactor.go`
  - `pkg/storage/.../tsdb/compactor.go`
- Update ~30+ import paths across codebase

## Result
Cleaner package hierarchy where compactor sits alongside other core components at `pkg/` level, while store-specific implementations stay with their respective stores.