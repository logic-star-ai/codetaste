# Title
Replace Redux with Zustand for state management

# Summary
Removed Redux (@reduxjs/toolkit, react-redux) and adopted Zustand for simpler, more modular state management across the Dashboard UI.

# Why
- Simplify state management architecture
- Reduce boilerplate (no reducers, actions, slices)
- Better modularity with separate stores per domain
- Improved TypeScript inference
- Smaller bundle size

# What Changed

### Dependencies
- **Removed**: `@reduxjs/toolkit`, `react-redux`, `redux`, `@types/react-redux`
- **Added**: `zustand@^5.0.5`

### Store Architecture
Replaced single Redux store with domain-specific Zustand stores:
- `zustand/auth.ts` → Authentication, tokens, namespace
- `zustand/component.ts` → Alerts, confirms, dialogs
- `zustand/experiment.ts` → Experiment creation flow state
- `zustand/setting.ts` → User preferences (debug mode, kube-system NS, ...)
- `zustand/system.ts` → System-level settings (theme, language)
- `zustand/workflow.ts` → Workflow editor state

### Deleted Files
- `src/store.ts`
- `src/reducers/index.ts`
- `src/slices/*.ts` (experiments, globalStatus, settings, workflows)

### Component Updates
- Changed `useStoreSelector` → `useXxxStore((state) => state.field)`
- Changed `useStoreDispatch()` → `useXxxActions()`
- Direct state mutations replaced with store actions
- ~60+ components updated

### API Layer
- `api/http.ts` → Removed error handling (moved to interceptors)
- `api/interceptors.ts` → Added `applyErrorHandling()` accepting dependencies

# Breaking Changes
⚠️ **Breaking**: Internal state management completely restructured. External APIs unaffected.

# Migration Pattern
```ts
// Before
const { theme } = useStoreSelector((state) => state.settings)
const dispatch = useStoreDispatch()
dispatch(setTheme('dark'))

// After  
const theme = useSystemStore((state) => state.theme)
const { setTheme } = useSystemActions()
setTheme('dark')
```