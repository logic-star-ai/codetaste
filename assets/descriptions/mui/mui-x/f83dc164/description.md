# Title
-----
[DataGrid] Remove legacy filtering API

# Summary
-------
Remove legacy filtering API (`getApplyFilterFn` and `getApplyQuickFilterFn` with `GridCellParams` signature) and promote V7 filtering API as the default.

# Why
---
- Simplify filtering API by removing dual support for legacy and V7 versions
- Improve performance by using more efficient signature as default
- Remove technical debt from maintaining two parallel APIs

# Changes
---------
**API Renames:**
- `getApplyFilterFnV7` → `getApplyFilterFn`
- `getApplyQuickFilterFnV7` → `getApplyQuickFilterFn`

**Removed Types:**
- `GetApplyFilterFnLegacy`
- `GetApplyQuickFilterFnLegacy`
- Legacy conversion utilities (`convertFilterV7ToLegacy`, `convertQuickFilterV7ToLegacy`, etc.)
- `GLOBAL_API_REF` and internal filter tagging utilities

**Signature Changes:**
```diff
- (params: GridCellParams) => boolean
+ (value, row, column, apiRef) => boolean
```

**Updated Components:**
- All filter operators (boolean, date, numeric, string, singleSelect)
- Aggregation wrapper for filters
- All documentation examples
- Migration guide entries

**Removed Documentation:**
- "Optimize performance" section (no longer needed with single API)