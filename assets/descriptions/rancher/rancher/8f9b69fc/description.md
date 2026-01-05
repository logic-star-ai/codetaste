# Refactor: Consolidate controllers and rename cluster context to user context

## Summary

Reorganize controller packages and rename `ClusterContext`/`WorkloadContext` to `UserContext`/`UserOnlyContext` across codebase. All controllers should be consolidated under `pkg/controllers/` with clear separation between management and user-scoped controllers.

## Why

Current package structure is fragmented with controllers scattered across multiple top-level packages (`pkg/cluster/controller`, `pkg/management/controller`, `pkg/workload/controller`, `pkg/helm/controller`, `pkg/catalog/controller`). This makes the codebase harder to navigate and maintain.

Naming is also unclear - `ClusterContext` and `WorkloadContext` don't clearly convey their actual scope and purpose.

## Changes

### Package Reorganization

- `pkg/cluster/controller/*` → `pkg/controllers/user/*`
- `pkg/management/controller/*` → `pkg/controllers/management/*`  
- `pkg/workload/controller/*` → `pkg/controllers/user/*`
- `pkg/helm/controller/*` → `pkg/controllers/user/helm/*`
- `pkg/catalog/controller/*` → `pkg/controllers/management/catalog/*`
- `pkg/api/cluster/*` → `pkg/api/user/*`

### Context Renaming

- `config.ClusterContext` → `config.UserContext`
- `config.WorkloadContext` → `config.UserOnlyContext`

### Cleanup

- Remove standalone main packages: `pkg/catalog/main.go`, `pkg/cluster/main.go`, `pkg/helm/main.go`, `pkg/management/main.go`, `pkg/workload/main.go`, `pkg/api/cluster/main.go`
- `server/proxy/proxy.go` → `pkg/proxy/proxy.go`
- `pkg/cluster/utils/*` → `pkg/ticker/*`
- Remove `pkg/workload/converttypes/*` - use `norman/types/convert/schemaconvert` instead

### Import Updates

All imports updated throughout codebase to reflect new package locations.