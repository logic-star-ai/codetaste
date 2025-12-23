# Refactor page state management from atoms to DI services

## Summary

Replace global Jotai atoms (`pageSettingsAtom`, `currentPageIdAtom`, `currentModeAtom`) with DI-scoped services to enable multiple workspace instances.

## Why

Global atoms prevent proper workspace isolation - when multiple workspaces are open, page state conflicts occur since atoms are shared globally across all instances.

## Changes

**Removed atoms:**
- `pageSettingsAtom` - stored page mode (page/edgeless) globally
- `currentPageIdAtom` - tracked current page ID globally  
- `currentModeAtom` - derived current page mode from pageSettingsAtom
- `pageSettingFamily` - atom family for per-page settings

**New services:**
- `PageRecord` - encapsulates page metadata, mode, title as reactive LiveData
- `PageRecordList` - manages all PageRecords per workspace
- `WorkspaceLocalState` - stores page mode keyed by `page:${id}:mode`

**Updated patterns:**
- `useAtomValue(currentModeAtom)` → `useLiveData(page.mode)`
- `pageSettingFamily(pageId)` → `pageRecordList.record(pageId).value`
- `setPageModeAtom` → `page.setMode()` / `page.toggleMode()`
- Components now consume `Page` service via DI instead of reading atoms

**Infrastructure:**
- Move initialization logic from `blocksuite/initialization` to root `infra/initialization`
- `useLiveData` now accepts `null | undefined` inputs
- `PageManager.open()` takes pageId string instead of PageMeta object

## Benefits

- Each workspace has isolated page state
- Better testability via DI
- Reactive state with LiveData observables
- Type-safe service access