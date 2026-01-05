# Title
Migrate from `$locale` global property to `i18n` composable

## Summary
Replace the deprecated `$locale` global property pattern with the modern `i18n` composable throughout the editor-ui codebase to align with Vue 3 composition API best practices.

## Why
- `$locale` as a global property is a Vue 2 pattern that doesn't fit well with Vue 3 composition API
- Composables provide better type safety, testability, and explicit dependencies
- Eliminates the need for `I18nPlugin` installation step
- Makes i18n usage more consistent across the codebase

## Changes

### Plugin & Setup
- Remove `I18nPlugin` from `main.ts` and test render setup
- Remove `$locale: I18nClass` from Vue's `ComponentCustomProperties` type definition

### Component Updates
- Import `useI18n` composable: `import { useI18n } from '@/composables/useI18n'`
- Initialize in setup: `const i18n = useI18n()`
- Replace all template/script references:
  - `$locale.baseText(...)` → `i18n.baseText(...)`
  - `$locale.nodeText()` → `i18n.nodeText()`
  - `$locale.credText()` → `i18n.credText()`
  - `$locale.localizeNodeName(...)` → `i18n.localizeNodeName(...)`
  - etc.

### Scope
~100+ component files affected across:
- Components (`/components/**`)
- Views (`/views/**`)
- Canvas elements
- Modals & dialogs
- Settings panels
- ...