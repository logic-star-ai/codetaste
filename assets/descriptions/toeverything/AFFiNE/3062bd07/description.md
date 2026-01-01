# Title
Remove global types from edgeless implementation

# Summary
Refactor edgeless block types from global `BlockSuite.*` namespace declarations to explicit type imports and exports. Eliminates ambient type declarations across surface elements, blocks, and related utilities.

# Why
- Global namespace (`BlockSuite.*`) creates implicit dependencies and pollutes global scope
- Type safety and IDE support degraded by ambient declarations
- Explicit imports make type relationships and dependencies clear
- Reduces risk of type conflicts and naming collisions

# Changes Made
**Removed global declarations:**
- `BlockSuite.EdgelessBlockModelMap` → explicit imports
- `BlockSuite.SurfaceElementModelMap` → exported from `elements/index.ts`
- `BlockSuite.EdgelessTextModelMap` → `SurfaceTextModelMap` 
- `BlockSuite.SurfaceLocalModel` → `GfxLocalElementModel`
- `BlockSuite.EdgelessModelKeys` → `string` or specific types
- Deleted `affine/model/src/utils/global.ts` entirely

**Updated imports across:**
- `block-surface/src/...` (crud-extension, connector-manager, renderer, ...)
- All block models (attachment, bookmark, edgeless-text, embed-*, frame, image, latex, note)
- All element models (brush, connector, group, mindmap, shape, text)
- Clipboard, keyboard, frame-manager, gfx-tool extensions
- Widget components (element-toolbar, change-text-menu)

**New explicit exports:**
```typescript
export type SurfaceElementModelMap = { brush, connector, group, mindmap, shape, text }
export type SurfaceTextModelMap = { text, connector, shape, edgeless-text }
export type SurfaceTextModel = SurfaceTextModelMap[keyof ...]
```

# Technical Details
- Function signatures now use `GfxPrimitiveElementModel`, `GfxBlockElementModel`, `GfxLocalElementModel` from `@blocksuite/block-std/gfx`
- Type assertions updated from `BlockSuite.*` → explicit model types
- `getLastPropsKey()` signature changed from `BlockSuite.EdgelessModelKeys` → `string`