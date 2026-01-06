# Refactor: Consolidate database types and remove auto-generated schema

Migrate database type definitions from auto-generated `src/db.d.ts` to explicit table definitions in `src/schema/tables`, consolidating the `DB` interface in `src/schema/index.ts` and moving utility types to `src/sql-tools`.