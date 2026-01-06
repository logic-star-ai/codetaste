# Refactor: Consolidate controllers and rename cluster context to user context

Reorganize controller packages and rename `ClusterContext`/`WorkloadContext` to `UserContext`/`UserOnlyContext` across codebase. All controllers should be consolidated under `pkg/controllers/` with clear separation between management and user-scoped controllers.