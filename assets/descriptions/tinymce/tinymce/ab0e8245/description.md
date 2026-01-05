# Replace disabled APIs with enabled APIs

## Summary

Replace all `disabled`-based APIs with `enabled`-based APIs across toolbar buttons, menu items, dialog components, and editor UI. This includes flipping property semantics, consolidating enable/disable methods, and inverting boolean logic throughout.

## Changes

### Properties
- **`disabled: boolean`** → **`enabled: boolean`** (inverted logic)
- Affects: toolbar buttons, menu items, dialog components, autocompleter items

### Methods
- **`isDisabled()`** → **`isEnabled()`** (inverted return value)
- **`enable()` + `disable()`** → **`setEnabled(state: boolean)`** (unified method)
- **Dialog API**: `disable(name)` + `enable(name)` → **`setEnabled(name, state)`**

### Affected Components
- Toolbar: buttons, toggle buttons, split buttons, menu buttons
- Menu: items, nested items, toggle items, choice items, card items, autocomplete items
- Dialog: input, textarea, checkbox, button, selectbox, listbox, sizeinput, urlinput
- Dialog API instance methods
- Context menus & context forms
- Editor UI APIs (`editor.ui.*`)

## Implementation Notes

- Default state changed: `enabled: true` by default (previously `disabled: false`)
- All boolean logic inverted: `!enabled` ↔ `disabled`
- `setEnabled(true)` ≡ old `enable()`, `setEnabled(false)` ≡ old `disable()`
- Demo files, tests, and plugin UIs updated accordingly
- Changelog entry added

## API Impact

Breaking change for:
- `ToolbarButtonInstanceApi`, `MenuItemInstanceApi`, `DialogInstanceApi`
- Component specs: `ToolbarButtonSpec`, `MenuItemSpec`, `DialogComponentSpec`, etc.
- `EditorUiApi` methods