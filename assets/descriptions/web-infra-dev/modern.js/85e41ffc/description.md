Title
-----
Refactor `@modern-js/utils` package structure for better tree-shaking and maintainability

Summary
-------
Reorganize `@modern-js/utils` package to separate CLI, browser, and node utilities into distinct modules with explicit export paths.

Why
---
- Current structure mixes browser/node/CLI code, preventing effective tree-shaking
- Import paths lack clarity about runtime environment (browser vs node)
- Flat file structure makes package difficult to maintain

Changes
-------

**New Module Structure:**
- `@modern-js/utils` - core CLI utilities
- `@modern-js/utils/runtime/router` - router utilities (remix-router, nestedRoutes)
- `@modern-js/utils/runtime-browser` - browser-specific runtime (parsedJSONFromElement, etc.)
- `@modern-js/utils/runtime-node` - node-specific runtime (serializeJson, SSR utilities, useHeaders)
- `@modern-js/utils/chain-id` - ChainIdentifier exports
- `@modern-js/utils/logger` - logger utilities
- `@modern-js/utils/universal/plugin-dag-sort` - plugin DAG sorting

**Internal Reorganization:**
- Move CLI-related files to `src/cli/` directory
- Split `is/` utilities into `is/config.ts`, `is/env.ts`, `is/platform.ts`, `is/project.ts`, `is/type.ts`
- Consolidate get functions into `cli/get/` subdirectory
- Group constants in `cli/constants/`
- Separate runtime code: `runtime-browser/`, `runtime-node/`, `runtime/`

**Migration Required:**
- `@modern-js/utils/universal/remix-router` → `@modern-js/utils/runtime/router`
- `@modern-js/utils/universal/nestedRoutes` → `@modern-js/utils/runtime/router`
- `@modern-js/utils/universal/serialize` → `@modern-js/utils/runtime-node`
- `@modern-js/utils/runtime` → `@modern-js/utils/runtime-browser` (for browser APIs)
- `@modern-js/utils/ssr` → `@modern-js/utils/runtime-node`
- `@modern-js/utils/universal/pluginDagSort` → `@modern-js/utils/universal/plugin-dag-sort`
- `@modern-js/utils/constants` → `@modern-js/utils`
- `ChainIdentifier` from `@modern-js/utils` → `@modern-js/utils/chain-id`

**Benefits:**
- Better tree-shaking by isolating browser/node code
- Clearer import semantics (explicit runtime environment)
- Improved code organization and discoverability
- Reduced bundle size for applications