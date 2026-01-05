# Refactor build operation types to use type token pattern

## Summary
Reorganize rich build operation details/results types to decouple producer side (Gradle internals) from consumer side (build scan plugin) semantics using a type token pattern.

## Why
Current `BuildOperationDetails<R>` interface tightly couples producer and consumer concerns. Need clearer separation between:
- What Gradle produces (implementation)
- What build scan plugin consumes (contract interfaces)

## Changes

### New Type Token Pattern
- Introduce `BuildOperationType<D, R>` interface as type token
- Operations now define separate `Details` and `Result` interfaces (annotated `@UsedByScanPlugin`)
- Implementation moves to inner `DetailsImpl`/`ResultImpl` classes
- `BuildOperationDescriptor.Builder.details()` accepts `Object` instead of `BuildOperationDetails<?>`

### Migrated Operation Types
Refactor all rich build operation types to new pattern:
- `ApplyPluginBuildOperation{Details → Type}`
- `ApplyScriptPluginBuildOperation{Details → Type}`  
- `ConfigureProjectBuildOperation{Details → Type}`
- `CalculateTaskGraph{Details → BuildOperationType}`
- `SnapshotTaskInputs{OperationDetails → BuildOperationType}`
- `FinalizeBuildCacheConfiguration{Details → BuildOperationType}`
- `DownloadArtifactBuildOperation{Details → Type}`
- `ResolveArtifactsBuildOperation{Details → Type}`
- `TaskOperationDetails → ExecuteTaskBuildOperationDetails`
- `DownloadBuildOperationDetails → ExternalResourceDownloadBuildOperationType`

### Cleanup
- Remove `BuildOperationDetails<R>` and `NoResultBuildOperationDetails` interfaces
- Move `UsedByScanPlugin` annotation to base-services
- Move `TestBuildOperationExecutor` to `internal.operations` package
- Add `BuildOperationTypes` utility for type extraction
- Update all test fixtures and integration tests