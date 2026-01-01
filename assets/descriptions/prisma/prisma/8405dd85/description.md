Title
-----
Extract `@prisma/dmmf` and `@prisma/generator` packages for better modularity

Summary
-------
Create two new packages to extract common types and utilities from `@prisma/generator-helper`:
- `@prisma/dmmf` - DMMF types and utilities
- `@prisma/generator` - Generator configuration types and utilities

`@prisma/generator-helper` remains for backward compatibility with third-party generators using JSON-RPC interface.

Why
---
Current architecture bundles all types in `@prisma/generator-helper`, making it difficult to:
- Reuse DMMF types across different contexts
- Share generator configuration types
- Maintain clear separation of concerns

What Changed
------------
**New Packages:**
- `@prisma/dmmf` - Contains:
  - DMMF type definitions (`Document`, `Model`, `Field`, `Schema`, etc.)
  - `datamodelEnumToSchemaEnum()` conversion utility
  - Tests and build configuration

- `@prisma/generator` - Contains:
  - Generator configuration types (`GeneratorConfig`, `GeneratorOptions`, `GeneratorManifest`)
  - TypedSQL types (`SqlQueryOutput`, `QueryIntrospectionType`, etc.)
  - Data source types (`DataSource`, `EnvValue`, etc.)
  - Tests and build configuration

**Existing Package:**
- `@prisma/generator-helper` - Now:
  - Re-exports types from `@prisma/dmmf` and `@prisma/generator` for backward compatibility
  - Contains JSON-RPC implementation details
  - Maintains existing API surface

**Updates:**
- Updated imports across all packages (`@prisma/client`, `@prisma/cli`, `@prisma/internals`, `@prisma/migrate`)
- Added new packages to CI/CD workflows
- Updated ESLint rules allowlist
- Added TypeScript path mappings

Done When
---------
- [x] `@prisma/dmmf` package created with types and utilities
- [x] `@prisma/generator` package created with configuration types
- [x] `@prisma/generator-helper` refactored to use new packages
- [x] All imports updated across codebase
- [x] Tests added for new packages
- [x] CI/CD workflows updated
- [x] Backward compatibility maintained