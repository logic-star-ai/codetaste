# Replace hotkey scopes with focus stack (Part 5)

## Summary

Migrate remaining components from deprecated hotkey scopes API to focus stack API for more robust hotkey management. This part covers form field inputs, pages, dialogs, navigation drawer, and various other components.

## Components Migrated

### Form Field Inputs
- `FormBooleanFieldInput`, `FormDateTimeFieldInput`, `FormTextFieldInput`, `FormNumberFieldInput`, `FormRawJsonFieldInput`, `FormUuidFieldInput`
- `FormMultiSelectFieldInput`, `FormSelectFieldInput`, `FormSingleRecordPicker`
- Added `formFieldInputInstanceId` prop to `FormFieldInputInnerContainer`
- Replaced `usePreviousHotkeyScope` with `usePushFocusItemToFocusStack` / `useRemoveFocusItemFromFocusStackById`

### Pages
- `PageChangeEffect`: All page navigation now uses `resetFocusStackToFocusItem` instead of `setHotkeyScope`
- Added `PageFocusId` enum for: `Settings`, `CreateWorkspace`, `SignInUp`, `CreateProfile`, `InviteTeam`, `SyncEmail`, `PlanRequired`, `RecordShowPage`, `RecordIndex`
- Onboarding pages (`CreateProfile`, `InviteTeam`, `SyncEmails`): Replaced `useScopedHotkeys` with `useHotkeysOnFocusedElement`

### Dialog System
- `Dialog`: Replaced `useScopedHotkeys` with `useHotkeysOnFocusedElement` for `Enter` / `Escape` handlers
- `DialogManagerEffect`: Push/remove focus items instead of setting hotkey scope
- `useDialogManager`: Use focus stack methods for cleanup
- Added `DIALOG_FOCUS_ID` constant

### Keyboard Shortcut Menu
- `KeyboardShortcutMenuOpenContent`: Migrated to `useHotkeysOnFocusedElement` for `Escape`
- `useKeyboardShortcutMenu`: Push/remove focus items on open/close
- Added `KEYBOARD_SHORTCUT_MENU_INSTANCE_ID`

### Record Components
- `RecordBoardColumnHeader`: Replaced dropdown menu hotkey management with `Dropdown` component
- `RecordBoardColumnDropdownMenu`: Simplified to only render content (no overlay/positioning)
- `ActivityRichTextEditor`: Migrated `Escape` and wildcard key handlers to `useHotkeysOnFocusedElement`
- Replaced `RECORD_INDEX_FOCUS_ID` constant with `PageFocusId.RecordIndex` enum value

### Navigation Drawer
- `NavigationDrawerInput`: Added focus stack push/remove on focus/blur
- Migrated `Enter` / `Escape` to `useHotkeysOnFocusedElement`

### Aggregate Dropdowns
- `RecordBoardColumnHeaderAggregateDropdownMenuContent`, `RecordBoardColumnHeaderAggregateDropdownOptionsContent`
- `RecordTableColumnAggregateFooterDropdownSubmenuContent`, `RecordTableColumnAggregateFooterMenuContent`
- Removed `useScopedHotkeys` for `Escape` key (handled by dropdown system)

### Settings & Serverless Functions
- Removed hotkey scope initialization from serverless function tabs/pages
- `SettingsServerlessFunctionsNew`, `SettingsServerlessFunctionCodeEditorTab`, `SettingsServerlessFunctionSettingsTab`, `SettingsServerlessFunctionTestTab`

### AI Agent Chat
- `useAgentChat`: Migrated `Enter` handler to `useHotkeysOnFocusedElement`

## Hooks & Utilities Removed

- ❌ `useHotkeyScopeOnMount` - Deleted entirely
- ❌ `useScopedHotkeys` - Replaced with `useHotkeysOnFocusedElement`
- ❌ `useScopedHotkeyCallback` - No longer needed
- ❌ Test file: `useScopedHotKeys.test.tsx`

## Focus Component Types Added

Extended `FocusComponentType` enum with:
- `FORM_FIELD_INPUT`
- `KEYBOARD_SHORTCUT_MENU`
- `DIALOG`

## Testing Updates

- Updated keyboard shortcut menu tests to verify new focus stack behavior
- Removed `RootDecorator` hotkey initialization (no longer needed)
- Set `DEBUG_HOTKEY_SCOPE = false`

## Why

- Focus stack provides hierarchical, explicit focus management vs. implicit scope switching
- Prevents hotkey conflicts and race conditions
- Clearer component ownership of keyboard events
- Enables proper cleanup on unmount/blur