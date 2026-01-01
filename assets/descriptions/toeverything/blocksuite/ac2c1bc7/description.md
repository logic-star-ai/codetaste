# Refactor: Rename `affine:group` to `affine:frame`

## Summary
Rename block type from `affine:group` to `affine:frame` throughout the codebase, including models, components, types, tests, and documentation.

## Changes

### Core Renames
- `GroupBlockModel` → `FrameBlockModel`
- `GroupBlockComponent` → `FrameBlockComponent`
- `affine:group` flavour → `affine:frame`
- Custom element `<affine-group>` → `<affine-frame>`

### File Structure
- `packages/blocks/src/group-block/` → `frame-block/`
- `group-model.ts` → `frame-model.ts`
- `group-block.ts` → `frame-block.ts`

### Variables & Constants
- `groupId` → `frameId`
- `GROUP_MIN_LENGTH` → `FRAME_MIN_LENGTH`
- `tryUpdateGroupSize()` → `tryUpdateFrameSize()`

### Styling
- `.affine-group-block-container` → `.affine-frame-block-container`
- `AFFINE-GROUP` tag checks → `AFFINE-FRAME`

### Updates Across
- `__internal__/` utility functions & keyboard handlers
- Page block (default & edgeless modes)
- Selection managers
- Clipboard/paste operations
- Test suites
- Documentation & README examples

## Migration
Added migration logic in `workspace/migrations.ts` to automatically convert legacy `affine:group` blocks to `affine:frame` with version updates.

## Testing
- Unit test for migration: `packages/store/src/__tests__/migration.unit.spec.ts`
- Binary fixture: `ydocs/legacy-group.ydoc`
- All existing tests updated to use frame terminology