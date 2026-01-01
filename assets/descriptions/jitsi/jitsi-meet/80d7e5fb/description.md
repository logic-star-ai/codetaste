# Refactor middleware and reducer loading to be explicit

## Summary

Move from implicit to explicit loading of middlewares and reducers. Currently, each feature's `index.js` imports its own middleware/reducer files, causing circular dependencies and platform-specific code leaking across web/native boundaries. Consolidate all imports into platform-specific entry points.

## Why

- Implicit loading via `index.js` creates complex import cycles → hard-to-fix bugs
- Web-only features inadvertently imported on mobile → crashes
- Circular dependencies difficult to track and resolve
- Platform boundaries not enforced

## Solution

Create explicit import manifests at app entrypoint:
- `middlewares.{any|web|native}.js` 
- `reducers.{any|web|native}.js`

Each platform imports appropriate modules + shared (`any`) modules.

## Changes

**New files:**
- `react/features/app/middlewares.any.js` - shared middlewares
- `react/features/app/middlewares.web.js` - web-specific
- `react/features/app/middlewares.native.js` - native-specific  
- `react/features/app/reducers.{any|web|native}.js` - same pattern

**Cleanup:**
- Remove `import './middleware'` / `import './reducer'` from feature `index.js` files
- Delete `index.js` files that only existed for imports (e.g., `base/lastn`, `mobile/*/`, `external-api`, ...)
- Update imports throughout codebase: `from '../app'` → `from '../app/actions'`
- Remove app feature `index.js` as exemplar

**Dev tooling:**
- Enable webpack circular dependency detection

## Notes

First step toward eliminating `index.js` barrel exports entirely. Future work: remove action/actionType/component re-exports from index files.