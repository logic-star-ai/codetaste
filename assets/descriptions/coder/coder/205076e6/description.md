# Setup knip and remove unused code

## Summary
Configure knip to detect and remove unused exports, files, and dependencies across the codebase. Clean up dead code to improve maintainability and reduce bundle size.

## Why
- Accumulated unused code degrades codebase quality
- Unused dependencies increase bundle size and maintenance overhead
- Dead exports create confusion about what's actually used
- No automated tooling to catch unused code

## What Changed

**Tooling Setup**
- Added `.knip.jsonc` configuration
  - Entry points: `index.tsx`, `serviceWorker.ts`
  - Ignore generated files (`*Generated.ts`)
  - Allow unused type/interface exports within same file
- Added `knip` to lint pipeline (`pnpm lint`)
- Enabled `noUnusedImports` warning in biome config

**Removed Unused Exports**
- Changed exported functions/components to internal where not used externally
- E2E helpers: `currentUser`, `fillParameters`, ...
- API utilities: `isApiErrorResponse`, `selectGroupsByUserId`, ...
- UI components: `DialogOverlay`, `DialogClose`, `ChartStyle`, ...
- Page components: various `*PageView` exports changed to default exports
- Query keys and helper functions across API layer

**Removed Unused Files**
- `__mocks__/react-markdown.tsx`
- Icons: `GitlabIcon`, `MarkdownIcon`, `TerraformIcon`
- Components: `ChartSection`, `ResourcesSidebarContent`, `BuildRow`, `LastUsed`, `ProvisionerGroup`
- Test/entity helpers: unused mock entities

**Removed Unused Dependencies**
- Runtime: `canvas`, `chartjs-plugin-annotation`, `emoji-datasource-apple`, `@radix-ui/react-visually-hidden`, ...
- Dev: `@testing-library/react-hooks`, `storybook-react-context`, `ts-node`, ...
- ~15 dependencies removed total

**Removed Unused Imports**
- Biome auto-fixes for unused imports throughout

## Impact
- Smaller bundle size
- Clearer public API surface
- Easier maintenance (less code to reason about)
- Automated checks prevent future unused code accumulation