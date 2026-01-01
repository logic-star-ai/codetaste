# Remove GraphHopperStorage wrapper class

## Summary
Remove `GraphHopperStorage` class and replace with direct `BaseGraph` usage. Rename `GraphHopper#getGraphHopperStorage()` → `GraphHopper#getBaseGraph()`.

## Why
`GraphHopperStorage` was meant to manage all graphs (base+CH) but never fulfilled this purpose. Other storage components like location index and landmarks were never included. It ended up being just a bag holding references to `BaseGraph`, `EncodingManager`, and `StorableProperties` without representing any key concept.

## What Changed
- **Rename**: `getGraphHopperStorage()` → `getBaseGraph()` throughout codebase
- **Remove**: `GraphHopperStorage` class entirely
- **Remove**: `GraphBuilder` class → replaced with `BaseGraph.Builder`
- **Move**: Properties management code from `GraphHopperStorage` → `GraphHopper`
  - New methods: `createBaseGraphAndProperties()`, `loadBaseGraphAndProperties()`
  - String formatting methods moved to `GraphHopper`
- **Refactor**: CH/LM preparation handlers now receive `BaseGraph` + `StorableProperties` separately
- **Update**: GTFS readers now take `BaseGraph` + `EncodingManager` instead of `GraphHopperStorage`
- **Rename**: Test classes `GraphHopperStorageTest` → `BaseGraphTest`, etc.

## Result
Clearer separation of concerns: `BaseGraph` represents the road network, `EncodingManager` handles encoded values, `StorableProperties` manages metadata. No unnecessary wrapper class.