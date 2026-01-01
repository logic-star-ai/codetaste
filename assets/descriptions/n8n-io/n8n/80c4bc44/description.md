# Title
Port design-system components to Composition API

# Summary
Continue migration of design-system components from Options API to Composition API with improved TypeScript types and standards.

# Why
- Modernize codebase with Composition API patterns
- Improve type safety across components
- Enable stricter TypeScript compiler options
- Reduce type errors in design-system (down to 23)

# Changes
**Components Converted:**
- N8nCallout, N8nFormInput(s), N8nInfoAccordion, N8nLink, N8nMenu/MenuItem
- N8nNodeIcon, N8nNotice, N8nPulse, N8nRadioButton(s)
- N8nRecycleScroller, N8nResizeWrapper, N8nRoute, N8nSticky
- N8nTabs, N8nTags, N8nTree, N8nUserSelect
- Styleguide components (VariableTable, SpacingPreview)

**Standardization:**
- Replace `defineComponent` + Options API → `setup` script with `defineProps`/`defineEmits`
- Remove `Locale` mixin → `useI18n()` composable
- Convert `data()` → `ref()` / `computed()`
- Add proper TypeScript interfaces for all component props

**Type System:**
- Replace custom `RouteObject` with `RouteLocationNormalizedLoaded` from vue-router
- Remove `RouteTo` type, use `RouteLocationRaw` from vue-router
- Add `SelectSize` type and proper icon types
- Add `Validatable` type for form inputs
- Type all event emitters properly

**Code Quality:**
- Clean up unused variables (`_` for unused loop vars)
- Enable `noUnusedLocals` in tsconfig
- Fix ref positioning inconsistencies
- Improve computed return type annotations