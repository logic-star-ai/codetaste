# Title
Consolidate listener info into `ListenerInfo` interface and expose in factory contexts

## Summary
Refactor listener-related information (`direction`, `metadata`, `typedMetadata`, `isQuic`) from scattered context methods into a dedicated `ListenerInfo` interface, making it accessible across wider contexts including access loggers.

## Why
Listener properties like `direction` were only available in filter contexts but needed in other contexts (e.g., access loggers). Information was scattered across multiple methods on `FactoryContext` rather than grouped logically.

## What Changed
- Added `Network::ListenerInfo` interface with:
  - `metadata()` 
  - `typedMetadata()`
  - `direction()`
  - `isQuic()`
- Created `ListenerInfoImpl` implementation
- Replaced `FactoryContext` methods (`direction()`, `listenerMetadata()`, `listenerTypedMetadata()`, `isQuicListener()`) with single `listenerInfo()` method
- Updated all call sites:
  - `context.direction()` → `context.listenerInfo().direction()`
  - `context.listenerMetadata()` → `context.listenerInfo().metadata()`
  - `context.isQuicListener()` → `context.listenerInfo().isQuic()`
  - etc.

## Benefits
- Single source of truth for listener information
- Listener properties accessible in broader contexts
- Better encapsulation and cleaner API
- Foundation for future listener proto trimming