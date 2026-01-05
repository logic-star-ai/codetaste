# Remove `medusa-core-utils` package and redistribute utilities

## Summary
Remove the deprecated `medusa-core-utils` package and move its utilities to their appropriate locations (`@medusajs/utils` and `@medusajs/medusa`).

## Why
- Consolidate utility functions in dedicated packages
- Eliminate redundant/outdated package
- Improve package structure and maintainability
- Avoid http/net dependencies in pure utils package

## Changes

### Package Removal
- Delete `packages/medusa-core-utils` entirely
- Remove from all `package.json` dependencies

### Utility Redistribution
**→ `@medusajs/utils`:**
- `build-regexp-if-valid.ts` (+ tests)
- `parse-cors-origins.ts` (+ tests)
- `get-config-file.ts` (change to named export)
- `MedusaError`, `isDefined`, `createMedusaContainer`, etc.

**→ `@medusajs/medusa/utils`:**
- `GracefulShutdownServer` (tight coupling to server + http/net deps)

### Import Updates
Replace all imports:
```ts
// Before
import { ... } from "medusa-core-utils"

// After
import { ... } from "@medusajs/utils"
// or
import { GracefulShutdownServer } from "@medusajs/medusa/dist/utils/graceful-shutdown-server"
```

Affected files:
- `integration-tests/**`
- `packages/cli/medusa-cli/**`
- `packages/core/**`
- `packages/medusa/**`
- `packages/modules/**`
- `www/apps/book/**`