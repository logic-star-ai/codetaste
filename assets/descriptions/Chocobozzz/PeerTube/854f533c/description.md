# Remove circular dependency between `shared` and `server` folders

## Summary

Break circular dependency between `shared` ↔ `server` folders and introduce TypeScript project references for improved build performance.

## Why

- Files in `shared` were importing from `server`, while `server` imported from `shared`, creating a circular dependency
- TypeScript project references forbid such circular dependencies
- Using project references enables incremental compilation, rebuilding only modified projects and their dependents
- Significantly improves build performance by avoiding full source recompilation

## What Changed

**Moved utilities from `server` to `shared` to break circular imports:**
- `server/helpers/uuid.ts` → `shared/core-utils/uuid.ts` (buildUUID, uuidToShort, isShortUUID, shortToUUID)
- Crypto functions (sha256, sha1) → `shared/core-utils/crypto.ts`
- Path utilities (root, buildPath, getLowercaseExtension) → `shared/core-utils/path.ts`
- FFprobe utilities → `shared/extra-utils/ffprobe.ts` (ffprobePromise, getVideoStreamSize, getVideoFileFPS, ...)
- Test utilities (completeVideoCheck, makeFollowRequest, makePOSTAPRequest) → `server/tests/shared/`

**TypeScript project references:**
- Created `tsconfig.base.json` with shared compiler options
- Added `tsconfig.json` to `scripts/`, `server/`, `shared/` with explicit `references` declarations
- Updated root `tsconfig.json` to use project references
- Modified `.eslintrc.json` to include all project `tsconfig.json` files

**Build changes:**
- Updated `scripts/build/server.sh` to use `tsc -b --verbose` 
- Copy all `tsconfig.json` files to `dist/` for each project
- Added `*.tsbuildinfo` to `.gitignore`

**Import updates:**
- Updated ~50+ import statements across server controllers, helpers, models, tests to use new paths
- Changed relative imports to use `@shared/*` barrel exports where applicable

## Benefits

✓ Clean dependency graph: `scripts` → `server` → `shared`  
✓ Incremental TypeScript compilation  
✓ Faster rebuilds  
✓ Better separation of concerns