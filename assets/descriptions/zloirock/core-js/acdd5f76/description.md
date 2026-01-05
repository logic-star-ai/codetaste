# Refactor Typed Arrays: Extract `ArrayBuffer` Methods & Move to Separate Namespace

## Summary
Refactor typed arrays module structure by:
- Extracting `ArrayBuffer` methods (`constructor`, `isView`, `slice`) into separate modules
- Moving `ArrayBuffer` and `DataView` out of typed arrays namespace
- Reorganizing entry points and file structure for better granularity

## Changes

### Module Splitting
- Split `es.typed.array-buffer` into:
  - `es.array-buffer.constructor`
  - `es.array-buffer.is-view`
  - `es.array-buffer.slice`
- Rename `es.typed.data-view` → `es.data-view`

### Namespace Reorganization
- Move from `features/typed-array/array-buffer.*` → `features/array-buffer/*`
- Move from `features/typed-array/data-view.*` → `features/data-view/*`
- Create new entry points:
  - `core-js/es/array-buffer`
  - `core-js/es/data-view`

### Entry Points
Remove from `es/typed-array`:
```js
require('../modules/es.typed.array-buffer');
require('../modules/es.typed.data-view');
```

Add granular imports:
```js
core-js/features/array-buffer
core-js/features/array-buffer/constructor
core-js/features/array-buffer/is-view
core-js/features/array-buffer/slice
core-js/features/data-view
```

### Internal Refactoring
- Rename `internals/typed-array.js` → `internals/typed-array-constructor.js`
- Rename `isArrayBufferView` → `isView` in `array-buffer-view-core`
- Switch reference from `Uint8Array` → `Int8Array` in internal helpers

## Why
- `ArrayBuffer` and `DataView` are not typed arrays themselves
- Allow more granular imports (e.g., only `ArrayBuffer.isView`)
- Better separation of concerns
- Clearer module boundaries
- Enable tree-shaking of unused methods