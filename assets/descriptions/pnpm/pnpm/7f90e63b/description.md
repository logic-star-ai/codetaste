# Title

Refactor: Create centralized `@pnpm/error` package

## Summary

Create a new `@pnpm/error` package to centralize error handling across the pnpm codebase and refactor all packages to use it.

## Why

- Multiple packages had duplicate `PnpmError` class implementations
- Error code assignment was inconsistent (manual `err['code']` assignments with tslint disables)
- Error handling lacked type safety across packages
- `ERR_PNPM_` prefix was manually added everywhere

## Changes

**New Package:**
- Create `packages/error/` with centralized `PnpmError` class
- Constructor: `new PnpmError(code, message)` automatically prefixes with `ERR_PNPM_`

**Refactored Packages:**
- `@pnpm/config`: Replace manual error creation with `PnpmError`
- `@pnpm/default-reporter`: Use `PnpmError` type in error handling
- `@pnpm/filter-lockfile`: Replace error code assignment
- `@pnpm/headless`: Use `PnpmError` for outdated lockfile errors
- `@pnpm/local-resolver`: Replace manual error creation
- `@pnpm/lockfile-file`: Remove local `PnpmError`, use centralized version
- `@pnpm/npm-resolver`: Create specialized error classes extending `PnpmError`
- `@pnpm/package-is-installable`: Extend `PnpmError` for engine/platform errors
- `@pnpm/package-store`: Remove local error implementations
- `@pnpm/pnpm`: Use centralized error class throughout
- `@pnpm/read-importer-manifest`: Replace error creation
- `@pnpm/resolve-dependencies`: Use `PnpmError`
- `@pnpm/supi`: Remove local `PnpmError`, update all error handling
- `@pnpm/tarball-fetcher`: Remove local error class, create specialized errors

**Improvements:**
- Remove `tslint:disable-line` comments for error code assignments
- Type-safe error handling in tests
- Consistent error code format across codebase
- Specialized error classes for specific error types