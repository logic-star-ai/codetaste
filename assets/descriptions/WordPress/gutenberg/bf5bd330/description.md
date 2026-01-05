# Consolidate `ui/utils` into `utils` to remove `ui/` folder

## Summary

Move remaining utility files from `packages/components/src/ui/utils/` to `packages/components/src/utils/` and update all imports across the codebase. This completes the removal of the `ui/` folder structure (started in #52953).

## Why

The `ui/` folder is no longer needed and adds unnecessary overhead when auditing or looking for components. The folder grouping serves no architectural purpose and should be eliminated to simplify the component structure.

## Changes

### Files Moved
- `ui/utils/space.ts` → `utils/space.ts`
- `ui/utils/font-size.ts` → `utils/font-size.ts`  
- `ui/utils/get-valid-children.ts` → `utils/get-valid-children.ts`
- `ui/utils/use-responsive-value.ts` → `utils/use-responsive-value.ts`
- `ui/utils/types.ts` → `utils/types.ts`

### Consolidated
- `ui/utils/colors.js` merged into existing `utils/colors.js` (name conflict)
- Tests consolidated: `ui/utils/test/colors.js` + `utils/test/colors.js` → single test file
- Tests moved: `ui/utils/test/space.js` → `utils/test/space.js`

### Updated
- ~50+ import statements across components to reference new paths
- `docs/tool/manifest.js` to remove `ui/` exclusion
- Removed `ui/README.md`

## Testing

- [ ] All existing tests pass
- [ ] No runtime errors from import path changes
- [ ] Consolidated color utility tests cover both functions