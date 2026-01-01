# Refactor: Rename `use/` folder to `composables/` and consolidate composable functions

## Summary

Rename the `use/` folder to `composables/` to align with official Vue.js naming conventions. Additionally, migrate composable functions scattered in `/components/hook/` into the unified `composables/` directory.

## Why

Following Vue.js official terminology and best practices. The term "composables" is the formal name for reusable composition functions in Vue 3 (ref: https://ja.vuejs.org/guide/reusability/composables).

## Changes

**Directory restructure:**
- `packages/frontend/src/use/` → `packages/frontend/src/composables/`
- Move `components/hook/useLoading.ts` → `composables/use-loading.ts`

**Files affected:**
- `use-chart-tooltip.ts`
- `use-form.ts`
- `use-leave-guard.ts`
- `use-loading.ts` (moved from `/components/hook/`)
- `use-mutation-observer.ts`
- `use-note-capture.ts`
- `use-pagination.ts`
- `use-scroll-position-keeper.ts`
- `use-tooltip.ts`

**Import updates:**
Update all imports across ~50+ component/page files to reference new path:
- `@/use/use-*.js` → `@/composables/use-*.js`