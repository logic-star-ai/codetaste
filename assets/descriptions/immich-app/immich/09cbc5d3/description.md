# Title

Refactor: Consolidate database types and remove auto-generated schema

# Summary

Migrate database type definitions from auto-generated `src/db.d.ts` to explicit table definitions in `src/schema/tables`, consolidating the `DB` interface in `src/schema/index.ts` and moving utility types to `src/sql-tools`.

# Why

- Remove dependency on `kysely-codegen` auto-generation
- Establish single source of truth for database schema
- Improve type maintainability with explicit definitions
- Better code organization and discoverability

# What

**Remove:**
- `src/db.d.ts` (auto-generated file)
- `kysely:codegen` npm script

**Migrate:**
- `DB` interface → `src/schema/index.ts`
- `Generated`, `Timestamp`, `Int8` types → `src/sql-tools/types.ts`

**Update:**
- All imports from `src/db` → `src/schema` or `src/schema/tables/*.table`
- Repository imports (Access, Activity, Album, Asset, Audit, ...)
- Service imports (Library, Metadata, Person, Sync, Tag, ...)
- Test imports and factories

**Impact:**
- ~50+ files updated with new import paths
- All table types now explicitly defined
- No functional changes, pure refactor