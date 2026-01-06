# Split database-dependent types from `interfaces.ts` into `types-db.ts`

Extract all types in `packages/cli/src/interfaces.ts` that depend (directly or transitively) on database entities into a new file `packages/cli/src/types-db.ts`. Fold `workflows.types.ts` into `types-db.ts` as well.