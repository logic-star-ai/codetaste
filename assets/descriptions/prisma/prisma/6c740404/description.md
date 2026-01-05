# Title
Consolidate terminology: Use `binaryTarget` consistently instead of `platform`

## Summary
Refactor codebase to consistently use `binaryTarget` terminology instead of mixing `platform` and `binaryTarget` interchangeably. The term `platform` is ambiguous and used to mean different things in different contexts.

## Why
- `platform` is overloaded: used to refer to OS, binary target, and other concepts
- `binaryTarget` matches user-facing API (`binaryTargets` in schema.prisma)
- Less ambiguous → easier to search/replace if naming changes later
- Improves code clarity and maintainability

## Scope
**Core API Changes:**
- Rename `getPlatform()` → `getBinaryTargetForCurrentPlatform()`
- Rename type `Platform` → `BinaryTarget`  
- Rename array `platforms` → `binaryTargets`
- Rename `getPlatformInternal()` → `getBinaryTargetForCurrentPlatformInternal()`

**Files Renamed:**
- `platforms.ts` → `binaryTargets.ts`
- `platformRegex.ts` → `binaryTargetRegex.ts`

**Variable/Parameter Renames:**
- `platform` → `binaryTarget` (function parameters, local variables)
- `platforms` → `binaryTargets` (arrays/lists)
- `knownPlatforms` → `knownBinaryTargets`

**Affected Packages:**
- `@prisma/cli`
- `@prisma/client`  
- `@prisma/engines`
- `@prisma/fetch-engine`
- `@prisma/get-platform`
- `@prisma/internals`

**Note:** Error reporting backend uses `platform` field - intentionally NOT changed to avoid backend deployment coordination.