# Rename `@automattic/data` package to `@automattic/api-core`

## Summary

Rename `@automattic/data` package → `@automattic/api-core` to better reflect its purpose and scope.

## Changes

- Rename package directory: `packages/data/` → `packages/api-core/`
- Update package name in `package.json`: `@automattic/data` → `@automattic/api-core`
- Update all imports across codebase from `@automattic/data` → `@automattic/api-core`
- Update package references in:
  - `package.json` dependencies across ~15 packages
  - TypeScript project references (`tsconfig.json`)
  - ESLint configuration (`.eslintrc.js`)
- Update README to reflect broader scope (REST APIs in general, not just WordPress.com)

## Why

- **Better naming**: Package handles REST APIs across Automattic products, not just WordPress.com
- **Clearer purpose**: "API core" better describes centralized data fetching functions and type definitions
- **Architecture alignment**: Part of larger effort to reorganize data layer structure

## Affected Areas

- Domain search components
- Stepper flows (onboarding, new-hosted-site, etc.)
- Customer home cards
- Plans features
- Data stores package
- Domain search package
- ~40+ import statements updated