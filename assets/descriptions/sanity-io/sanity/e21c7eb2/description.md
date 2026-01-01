# Refactor: Move `@sanity/validation` into monopackage

## Summary

Move `@sanity/validation` package from standalone package into `sanity` monopackage as internal API at `src/core/validation/`

## Why

The exported validation API was never built for external consumption. It requires numerous internal dependencies that are cumbersome to provide outside a Sanity application:
- Schema instances
- Client getters  
- Document existence checks
- ... other internal context

By consolidating into the monopackage, we can treat it as the internal API it truly is.

## Changes

**Package structure:**
- Delete `packages/@sanity/validation/` directory entirely (package.json, configs, etc.)
- Move source: `packages/@sanity/validation/src/*` → `packages/sanity/src/core/validation/*`
- Move tests: `packages/@sanity/validation/test/*` → `packages/sanity/test/validation/*`

**Import updates:**
- Update all imports from `@sanity/validation` to `../validation` or `../../core/validation`
- Update JSDoc references: `@sanity/validation` → `sanity/validation`
- Remove `@sanity/validation` from dev aliases
- Remove `@sanity/validation` dependency from `packages/sanity/package.json`

**Config cleanup:**
- Remove TypeScript project references to `@sanity/validation`
- Remove from root `tsconfig.json` and `tsconfig.lib.json`

## Notes

A future version of `@sanity/validation` should be published indicating deprecation. The current published version should continue working for existing consumers. In time, we can work on exposing a simplified validation API meant for external consumption (node scripts, etc.).