# Refactor: Extract runtime utilities into separate package

## Summary

Split runtime-specific utilities from `@modern-js/utils` into a new dedicated package `@modern-js/runtime-utils` to improve modularity and maintainability.

## Why

- Runtime utilities were scattered across `@modern-js/utils` under various paths (`/runtime/*`, `/runtime-browser`, `/runtime-node`, etc.)
- Mixing runtime-specific code with general utilities reduced code organization
- Separate package enables better tree-shaking and clearer dependency boundaries

## Changes

**New Package**: `@modern-js/runtime-utils`

Extracted modules:
- `router` ← `@modern-js/utils/runtime/router`
- `remix-router` ← `@modern-js/utils/runtime/remix-router`
- `browser/*` ← `@modern-js/utils/runtime-browser`, `@modern-js/utils/runtime/nested-routes`
- `node/*` ← `@modern-js/utils/runtime-node/*`
- `time` ← `@modern-js/utils/universal/time`

**Updated packages** (imports + dependencies):
- `@modern-js/plugin-data-loader`
- `@modern-js/plugin-router-v5`
- `@modern-js/runtime`
- `@modern-js/create-request`
- `@modern-js/prod-server`
- `@modern-js/server`
- `@modern-js/app-tools`

**Package exports**:
- ESM + CJS dual support
- Entry points: `/router`, `/remix-router`, `/browser`, `/node`, `/node/router`, `/time`