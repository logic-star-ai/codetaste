# Refactor Vuetify interface to ease Vuetify 3 migration

## Summary

Abstract Vuetify 2 API usage behind composables that mirror Vuetify 3's interface, centralizing breakpoint logic and type imports to simplify future migration.

## Why

Vuetify 3 introduces breaking changes in API structure. By wrapping v2 APIs with v3-compatible interfaces now, the actual migration becomes a matter of updating the composable implementations rather than touching hundreds of component files.

## Changes

### `useDisplay()` composable
- Introduced new composable wrapping `$vuetify.breakpoint` API
- Returns reactive properties: `xs`, `sm`, `md`, `lg`, `xl`, `mobile`, `name`, `width`
- Returns helpers: `smAndDown`, `smAndUp`, `mdAndDown`, `mdAndUp`, `lgAndDown`, `lgAndUp`
- Matches Vuetify 3's display composable structure

### Type centralization
- Created `@/types/vuetify.ts` for local re-export of Vuetify types
- Changed all `DataTableHeader` imports from `'vuetify'` → `'@/types/vuetify'`
- Enables single-point type updates during migration

### Component updates
- Replaced `$vuetify.breakpoint.*` → `useDisplay()` across ~50+ components
- Replaced `currentBreakpoint.xsOnly` → `xs`
- Replaced `$vuetify.theme.dark` → `useTheme().dark`
- Cleaned up `useTheme()` composable (moved breakpoint logic to `useDisplay()`)

### Plugin exports
- Changed vuetify plugin from default export to named export

## Scope

Frontend only. No functional changes—purely structural refactoring for migration preparation.