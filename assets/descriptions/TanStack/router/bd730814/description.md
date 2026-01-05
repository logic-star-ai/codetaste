# Migrate shared types from react-router and solid-router to router-core

## Summary
Begin consolidation of duplicate type definitions by migrating common types from `react-router` and `solid-router` packages into the central `router-core` package.

## Why
- Eliminate type duplication between React and Solid router implementations
- Centralize shared type definitions for better maintainability
- Enable type reuse across framework-specific router packages

## Changes

### Types Migrated to `router-core`
- **Link types**: `NavigateOptions`, `ToOptions`, `LinkOptions`, `MaskOptions`, `ToPathOption`, `SearchParamOptions`, `PathParamOptions`, `MakeOptionalPathParams`, `ResolveRoute`, `RelativeToPath*`, `AbsoluteToPath`, etc.
- **Route info types**: `ParseRoute`, `RouteById`, `RouteIds`, `RoutePaths`, `RoutesById`, `RoutesByPath`, `AllParams`, `AllContext`, `AllLoaderData`, `FullSearchSchema`, `FullSearchSchemaInput`, etc.
- **Route types**: `RouteTypes`, `ResolveFullSearchSchema`, `ResolveFullSearchSchemaInput`, `ResolveAllContext`, `RouteContextParameter`, `BeforeLoadContextParameter`, `ResolveAllParamsFromParent`, `FullSearchSchemaOption`, `RemountDepsOptions`, `MakeRemountDepsOptionsUnion`, `ResolveFullPath`, `AnyRoute`, `Route`, `RootRoute`, `AnyRouteWithContext`
- **Router types**: `Register`, `AnyRouter`, `AnyRouterWithContext`, `RouterOptions`, `Router`
- **File route types**: `FileRoutesByPath`, `FileRouteTypes`, `InferFileRouteTypes`
- **Provider types**: `NavigateFn`, `BuildLocationFn`, `CommitLocationOptions`, `MatchLocation`

### Implementation
- Route classes now implement core interfaces (`CoreRoute`, `CoreRootRoute`)
- Updated all imports across `react-router` and `solid-router` to reference `@tanstack/router-core`
- Re-export migrated types from package index files
- Module augmentation moved to `@tanstack/router-core`

### Deleted Files
- `react-router/src/routeInfo.ts` → migrated to `router-core/src/routeInfo.ts`
- `solid-router/src/routeInfo.ts` → migrated to `router-core/src/routeInfo.ts`

## Status
⚠️ **Partial migration** - many more types remain to be migrated in follow-up work