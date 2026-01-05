# Refactor: Remove dependency on static Scene

## Summary

Remove static `Scene` methods (`Scene.getScene()`, `Scene.mapElementToScene()`) and pass `scene` or `elementsMap` explicitly throughout the codebase instead of relying on global lookups.

## Why

- Enable `@excalidraw/element` functions (e.g., `change`) to work **server-side** without providing/updating a global Scene
- Eliminate static state and improve testability
- Better separation of concerns between elements and scene management

## Changes

### Breaking Changes

- **`mutateElement` no longer informs mutation by default**
  - Previously: `mutateElement(element, updates)` would trigger re-render
  - Now: `mutateElement(element, elementsMap, updates)` does NOT trigger re-render
  - Use `scene.mutateElement(element, updates)` or `excalidrawAPI.mutateElement(element, updates)` instead

### Implementation

- [x] Move `Scene` from `packages/excalidraw/scene/` to `packages/element/src/`
- [x] Remove static methods: `Scene.getScene()`, `Scene.mapElementToScene()`
- [x] Update all functions to accept `scene` parameter instead of looking it up statically:
  - `bindOrUnbindLinearElement(..., scene)`
  - `updateBoundElements(..., scene)`
  - `alignElements(..., scene)`
  - `redrawTextBoundingBox(..., scene)`
  - `handleBindTextResize(..., scene)`
  - ... (many more)
- [x] Add `scene.mutateElement()` method
- [x] Add `excalidrawAPI.mutateElement()` to public API
- [x] Update all call sites throughout codebase
- [x] Update tests

### Migration Guide

**Before:**
```ts
mutateElement(element, { x: 100 }); // triggers re-render
```

**After:**
```ts
// Option 1: Use scene.mutateElement (triggers re-render)
scene.mutateElement(element, { x: 100 });

// Option 2: Use API (triggers re-render)
excalidrawAPI.mutateElement(element, { x: 100 });

// Option 3: Direct mutation (no re-render)
mutateElement(element, elementsMap, { x: 100 });
```