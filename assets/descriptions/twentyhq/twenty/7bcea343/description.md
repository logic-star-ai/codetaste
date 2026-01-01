# Refactor hotkeys into dedicated lib folder with scoped enums

## Summary
Refactor hotkey management system by:
- Moving from `@/hotkeys` → `@/lib/hotkeys`
- Breaking down monolithic `InternalHotkeysScope` enum into domain-specific enums
- Removing external dependencies from hotkeys module
- Standardizing naming from plural "hotkeys*" to singular "hotkey*"

## Why
- **Isolation**: Hotkeys should be a standalone library without dependencies on other modules
- **Maintainability**: Adding new hotkey scopes shouldn't require touching `lib/hotkeys`
- **Organization**: Hotkey scopes should live with their respective domains
- **Consistency**: Internal files properly scoped in `internal/` folders

## Changes

### Module relocation
- `@/hotkeys/*` → `@/lib/hotkeys/*`
- Internal files moved to `internal/` subdirectory

### Scope enum decomposition
Split `InternalHotkeysScope` into domain-specific enums:
- `AppHotkeyScope` - app-level scopes (App, CommandMenu, Goto)
- `TableHotkeyScope` - table interactions (Table, TableSoftFocus, CellEditMode, ...)
- `RelationPickerHotkeyScope` - relation picker
- `BoardCardFieldHotkeyScope` - board card field editing
- `FiltersHotkeyScope` - filter dropdown
- `InputHotkeyScope` - text input
- `RightDrawerHotkeyScope` - right drawer
- `PageHotkeyScope` - page-specific scopes (Settings, CreateWorkspace, ...)

### Naming standardization
- `useSetHotkeysScope` → `useSetHotkeyScope`
- `usePreviousHotkeysScope` → `usePreviousHotkeyScope`
- `useHotkeysScopes` → `useHotkeyScopes`
- `useHotkeysScopeAutoSync` → `useHotkeyScopeAutoSync`
- `HotkeysScope` → `HotkeyScope`
- `CustomHotkeysScopes` → `CustomHotkeyScopes`
- `currentHotkeysScopeState` → `currentHotkeyScopeState`
- `setHotkeysScopeAndMemorizePreviousScope` → `setHotkeyScopeAndMemorizePreviousScope`
- `goBackToPreviousHotkeysScope` → `goBackToPreviousHotkeyScope`
- Various component props: `editHotkeysScope` → `editHotkeyScope`, `hotkeysScope` → `HotkeyScope`

### File structure
```
lib/hotkeys/
├── constants/index.ts
├── hooks/
│   ├── internal/
│   │   ├── useHotkeyScopeAutoSync.ts
│   │   ├── useHotkeyScopes.ts
│   ├── usePreviousHotkeyScope.ts
│   ├── useSetHotkeyScope.ts
│   ├── useScopedHotkeys.ts
│   ├── useSequenceScopedHotkeys.ts
│   └── useGoToHotkeys.ts
├── states/internal/...
└── types/
    ├── AppHotkeyScope.ts
    ├── CustomHotkeyScope.ts
    └── HotkeyScope.ts
```

Domain-specific scopes now live with their domains:
- `@/relation-picker/types/RelationPickerHotkeyScope.ts`
- `@/ui/tables/types/TableHotkeyScope.ts`
- `@/ui/board-card-field/types/BoardCardFieldHotkeyScope.ts`
- ...