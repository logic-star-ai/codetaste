# Rename `@apollo/client/link/core` entrypoint to `@apollo/client/link`

## Summary
Rename the `@apollo/client/link/core` entrypoint to `@apollo/client/link` to simplify the import path for core link functionality.

## Why
- Simplify import paths for link-related imports
- Remove unnecessary `/core` suffix from the main link entrypoint
- More intuitive naming convention aligned with other entrypoints

## Changes
- Rename `src/link/core/index.ts` → `src/link/index.ts`
- Update package.json exports: `./link/core` → `./link`
- Update all internal imports from `@apollo/client/link/core` → `@apollo/client/link`
- Update API reports across all link packages (batch, batch-http, context, error, http, persisted-queries, remove-typename, retry, schema, subscriptions, utils, ws)
- Update test imports throughout codebase

## Affected Imports
- `ApolloLink`
- `concat`, `empty`, `from`, `split`, `execute`
- `FetchResult`, `Operation`, `NextLink`, `GraphQLRequest`, `OperationContext`
- `ExecutionPatch*`, `DocumentNode`, `Path`, `RequestHandler`, `SingleExecutionResult`
- ...and related types

## Breaking Change
**Major:** Users must update imports from `@apollo/client/link/core` → `@apollo/client/link`