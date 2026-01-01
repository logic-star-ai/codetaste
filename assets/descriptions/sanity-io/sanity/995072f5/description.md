# Refactor perspective hooks and add provider for better composability

## Summary

Split `usePerspective` into smaller, focused hooks and introduce `PerspectiveProvider` to enable perspective value overrides in specific contexts (e.g., diff modals, history views).

## Changes

**Provider Architecture**
- Add `PerspectiveProvider` for local perspective context overrides
- Add `GlobalPerspectiveProvider` (used in `StudioProvider`) that reads from router
- Add `PerspectiveContext` singleton

**Hook Separation**
- `usePerspective()` → returns read-only perspective values
  - `selectedPerspective`
  - `selectedPerspectiveName` 
  - `selectedReleaseId`
  - `perspectiveStack`
  - `excludedPerspectives`
- `useSetPerspective()` → returns `setPerspective` function
- `useExcludedPerspective()` → returns `excludedPerspectives`, `toggleExcludedPerspective`, `isPerspectiveExcluded`

**Types Moved**
- Extract `PerspectiveContextValue`, `PerspectiveStack`, `SelectedPerspective` to `core/perspective/types.ts`

## Why

- **Separation of concerns**: Read operations vs write operations in separate hooks
- **Override capability**: Provider allows forcing perspective values in specific contexts (history timeline, diff modals)
- **Better composability**: Components only import what they need
- **Cleaner architecture**: Align with React context/provider patterns