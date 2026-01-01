# Refactor Model_Infotable and Model_Setting API naming conventions

## Summary
Standardize method naming across `Model_Infotable` and `Model_Setting` classes to improve code consistency and readability. Rename ~20 methods to follow consistent get/set conventions with type-specific method names.

## Why
Current naming is inconsistent:
- Mixed PascalCase/camelCase (`GetStringInfo` vs `Theme`)
- Unclear method purposes (`Set` for multiple types)
- Inconsistent verb usage (`ContainsSetting` vs `KeyExists`)

New naming provides:
- Consistent camelCase convention
- Clear get/set prefixes
- Type-specific method names
- Improved API clarity

## Changes

**Model_Infotable:**
- `KeyExists()` → `contains()`
- `Set(..., wxString)` → `setRaw()` / `setString()`
- `GetStringInfo()` → `getRaw()` / `getString()`
- `Set(..., int)` → `setInt()`, `Set(..., bool)` → `setBool()`, etc.
- `GetIntInfo()` → `getInt()`, `GetBoolInfo()` → `getBool()`, etc.
- Add: `setArrayString()`, `setSize()`, `setColour()`, `setDate()`
- `FindLabelInJSON()` → `findArrayItem()`
- `Update()` → `updateArrayItem()`
- `Prepend()` → `prependArrayItem()`
- `Erase()` → `eraseArrayItem()`
- `OpenCustomDialog()` → `getOpenCustomDialog()` / `setOpenCustomDialog()`
- `CustomDialogSize()` → `getCustomDialogSize()` / `setCustomDialogSize()`

**Model_Setting:**
- `ContainsSetting()` → `contains()`
- `Set(..., wxString)` → `setRaw()` / `setString()`
- `Get*Setting()` → `get*()`
- Add: `getColour()`, `setArrayString()`
- `GetViewAccounts()` → `getViewAccounts()` / `setViewAccounts()`
- `Theme()` → `getTheme()` / `setTheme()`
- `ViewTransactions()` → `getViewTransactions()` / `setViewTransactions()`
- `ShrinkUsageTable()` → `shrinkUsageTable()`

## Impact
~70 files updated across codebase with no functional changes.