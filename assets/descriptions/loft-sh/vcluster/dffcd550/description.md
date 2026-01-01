# Refactor: Make syncer generic

## Summary
Restructure syncer interface to use Go generics, eliminating manual type casting and improving type safety across all resource syncers.

## Why
- Current syncer methods accept `client.Object`, requiring manual type casting in every implementation
- Cast operations are error-prone and add boilerplate code
- Event source/target determination logic scattered across sync methods
- `synccontext.Cast()` and `SyncSourceTarget()` helper functions needed in every syncer

## Changes

### Core Interface
- Add `Syncer()` method returning `Sync[client.Object]` to syncer interface
- Introduce generic event types: `SyncEvent[T]`, `SyncToHostEvent[T]`, `SyncToVirtualEvent[T]`
- Events encapsulate: type, source, host/virtual objects
- Replace method signatures:
  - `SyncToHost(ctx, vObj client.Object)` → `SyncToHost(ctx, event *SyncToHostEvent[T])`
  - `Sync(ctx, pObj, vObj client.Object)` → `Sync(ctx, event *SyncEvent[T])`
  - `SyncToVirtual(ctx, pObj client.Object)` → `SyncToVirtual(ctx, event *SyncToVirtualEvent[T])`

### Event API
- `event.SourceObject()` / `event.TargetObject()` - automatic based on sync direction
- `event.IsDelete()` - check for deletion events
- Remove `synccontext.Cast()`, `SyncSourceTarget()`, `EventFromHost()`, `EventFromVirtual()`

### Implementation
- Update all resource syncers: pods, services, configmaps, secrets, pvcs, pvs, ingresses, endpoints, nodes, namespaces, storage classes, CSI resources, volume snapshots, ...
- Add `ToGenericSyncer[T]()` wrapper for type conversion
- Test helpers: `NewSyncEvent()`, `NewSyncToHostEvent()`, `NewSyncToVirtualEvent()`

## Benefits
- ✅ Type-safe syncer implementations
- ✅ No manual casting required
- ✅ Clearer sync direction and event handling
- ✅ Less boilerplate code
- ✅ Reduced error surface