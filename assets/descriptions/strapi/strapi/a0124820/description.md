# Migrate database package to TypeScript

## Summary
Migrate the `@strapi/database` package from JavaScript to TypeScript while maintaining existing public API and behavior.

## Details
- Convert all `.js` files in `lib/` to `.ts` files in `src/`
- Add TypeScript type definitions throughout codebase
- Migrate from CommonJS (`module.exports`) to ES modules (`export`)
- Update build configuration:
  - Add `tsconfig.json`, `tsconfig.build.json`, `tsconfig.eslint.json`
  - Add `packup.config.ts` for bundling
  - Update `package.json` main/module/types entries to point to `dist/`
- Update ESLint config to use TypeScript rules (`custom/back/typescript`)
- Add proper type annotations for:
  - Database core (`index.ts`, `connection.ts`, `transaction-context.ts`)
  - Query builder and helpers
  - Entity manager and repositories
  - Schema builder and diff utilities
  - Metadata and relations
  - Field types and validators
  - Dialects (MySQL, PostgreSQL, SQLite)
  - Lifecycle system
  - Migrations

## Notes
- Public interface kept as "almost everything is any" initially
- Types will need gradual improvement to support entityService/documentService
- No breaking changes to existing functionality
- Build output in `dist/` directory (gitignored)