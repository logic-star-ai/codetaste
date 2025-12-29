# Refactor: Add enums for Affine palette colors and styles

## Summary
Replace string literals and array indices with TypeScript enums for palette colors and styles. Move color/style constants to `affine-model/consts` and consolidate duplicate type definitions.

## Why
Current implementation uses magic strings and array indices, making code hard to read and maintain:
```typescript
// Before
mode === 'dark' ? LINE_COLORS[10] : LINE_COLORS[8];
fillColor: '--affine-palette-shape-yellow'
```

Enums provide better readability and type safety:
```typescript
// After
mode === 'dark' ? LineColor.White : LineColor.Black;
fillColor: ShapeFillColor.Yellow
```

## Changes
- Add enums: `LineColor`, `ShapeFillColor`, `NoteBackgroundColor`, `NoteShadow`, `ShapeType`, `ShapeStyle`
- Create `affine-model/src/consts/line.ts` with line color definitions
- Update `note.ts` and `shape.ts` in `affine-model/consts` with enum-based constants
- Move `zod.ts` utility from `affine-shared` to `affine-model`
- Remove duplicate `ShapeType` and `ShapeStyle` types from `utils/types.ts`
- Update all references across:
  - `surface-block/*`
  - `root-block/edgeless/*`
  - `blocks/src/*`
  - Replace string literals with enum values
  - Replace array index access with named enum members

## Affected Areas
- Color panel components
- Shape/connector toolbars
- Auto-complete panels
- Element renderers
- Mind map drawing
- Edit session management
- ~200+ file references updated