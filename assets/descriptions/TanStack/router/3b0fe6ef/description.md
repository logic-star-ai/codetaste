# Refactor(router-core): Extract framework-agnostic logic into separate package

## Summary
Extract shared router logic from `react-router` into new `@tanstack/router-core` package. Maintain backwards compatibility via re-exports.

## Why
Preparation step for framework-agnostic router implementation. Separates core routing logic from React-specific code, enabling reuse across different frameworks.

## Changes
**New package: `@tanstack/router-core`**
- Moved files: `defer`, `location`, `manifest`, `path`, `qss`, `root`, `searchMiddleware`, `searchParams`, `serializer`, `validators`, test files
- Extracted types/utilities:
  - `Matches.ts` - `isMatch` logic
  - `link.ts` - link types (`ActiveOptions`, `LinkOptionsProps`, `ResolveRelativePath`, etc.)
  - `route.ts` - route types (`AnyPathParams`, `SearchSchemaInput`, `ResolveParams`, `ParamsOptions`, etc.)
  - `router.ts` - `ViewTransitionOptions`, `defaultSerializeError`, `TrailingSlashOption`, etc.
  - `RouterProvider.ts` - `CommitLocationOptions`, `MatchLocation`
  - `structuralSharing.ts` - `OptionalStructuralSharing`
  - `utils.ts` - utility functions/types

**Updated `react-router`**
- Imports from `@tanstack/router-core` instead of local files
- Re-exports all router-core types/functions in `index.tsx` for backwards compatibility
- No breaking changes to public API

**Package setup**
- Added router-core to workspace dependencies
- Updated publish script to include router-core
- Added tsconfig, vite config, eslint config for new package