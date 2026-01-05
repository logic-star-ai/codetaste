# Title
-----
Refactor relation picker to record picker and migrate from scope-based to component instance state management

# Summary
-------
Rename relation picker components/hooks to "record picker" when only selecting records (not managing relations). Remove scope-based state management in favor of component instance contexts. Standardize "entity" terminology to "record" throughout.

# Why
---
- Prepare record picker for reuse in workflows
- Improve semantic clarity: "record picker" when selecting records, not managing relations
- Modernize state management: replace Recoil scopes with component instance pattern
- Consistent naming: align with codebase conventions (record over entity)

# Changes
---------
**Components:**
- `RelationPickerScope` → `RecordPickerComponentInstanceContext.Provider`
- `SingleEntitySelect` → `SingleRecordSelect`
- `SingleEntitySelectMenuItems*` → `SingleRecordSelectMenuItems*`
- ...

**Hooks:**
- `useEntitySelectSearch` → `useRecordSelectSearch`
- `useRelationPicker` → `useRecordPicker`
- `useRelationPickerEntitiesOptions` → `useRecordPickerRecordsOptions`
- `useFilteredSearchEntityQuery` → `useFilteredSearchRecordQuery`
- ...

**Types:**
- `EntityForSelect` → `RecordForSelect`
- `EntitiesForMultipleEntitySelect` → `RecordsForMultipleRecordSelect`

**Props/Variables:**
- `relationPickerScopeId` → `recordPickerInstanceId`
- `relationObjectNameSingular` → `objectNameSingular`
- `selectedRelationRecordIds` → `selectedRecordIds`
- `excludedRelationRecordIds` → `excludedRecordIds`
- `entitiesToSelect` → `recordsToSelect`
- `onEntitySelected` → `onRecordSelected`
- ...

**State Management:**
- Remove scope-based states (`*ScopedState`)
- Add component states V2 (`*ComponentState`)
- Replace `useAvailableScopeIdOrThrow` with `useAvailableComponentInstanceIdOrThrow`
- Delete `RelationPickerScopeInternalContext`, `useRelationPickerScopedStates`, `getRelationPickerScopedStates`