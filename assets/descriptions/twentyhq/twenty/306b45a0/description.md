# Refactor Multiple Record Actions and No Selection Actions

## Summary

Refactor multiple record actions and no selection record actions to use config files, following the same pattern as single record actions. This consolidates action registration logic and reduces code duplication.

## Changes

### Architecture
- Consolidated action configs into centralized files:
  - `DefaultActionsConfigV1/V2.ts`
  - `WorkflowActionsConfig.ts`
  - `WorkflowRunsActionsConfig.ts`
  - `WorkflowVersionsActionsConfig.ts`
- Created `RegisterRecordActionEffect` component for unified action registration
- Simplified `RecordActionMenuEntriesSetter` to use new registration system

### Action Hooks
- Renamed type: `SingleRecordActionHook` → `ActionHook`
- Removed `recordId` parameter from all action hooks
- Added `useSelectedRecordIdOrThrow()` to extract recordId from context
- Updated all hooks:
  - `useDeleteMultipleRecordsAction`
  - `useExportMultipleRecordsAction`
  - `useAddToFavoritesSingleRecordAction`
  - `useDeleteSingleRecordAction`
  - `useDestroySingleRecordAction`
  - `useExportNoteAction`
  - `useNavigateToNextRecordSingleRecordAction`
  - `useNavigateToPreviousRecordSingleRecordAction`
  - `useRemoveFromFavoritesSingleRecordAction`
  - All workflow-related action hooks

### Removed Components
- `MultipleRecordsActionMenuEntrySetterEffect`
- `NoSelectionActionMenuEntrySetterEffect`
- `SingleRecordActionMenuEntrySetterEffect`
- `useMultipleRecordsActions`
- `useNoSelectionRecordActions`
- `useExportViewNoSelectionRecordAction`
- `useActionMenuEntriesWithCallbacks`

### Utilities
- Added `getActionViewType()` helper
- Updated `getActionConfig()` to use switch statement

### Tests
- Updated tests to focus on action behavior (onClick) rather than registration/unregistration
- Added `contextStoreNumberOfSelectedRecords` to test helpers

## Why

- **Consistency**: All action types now follow the same config-based pattern
- **Maintainability**: Centralized configs make actions easier to find and modify
- **Simplicity**: Reduced registration logic from multiple components to single unified approach
- **Less duplication**: Removed redundant setter effects and registration hooks