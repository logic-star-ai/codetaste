# Title
Refactor exporting modules to class pattern

# Summary
Convert exporting functionality from Chart prototype methods to dedicated `Exporting` class with instance methods, improving modularity and separation of concerns.

# Why
The current implementation mixes core chart functionality with optional exporting features by having exporting methods directly on the Chart prototype. This refactoring separates concerns by moving all exporting logic into a dedicated `Exporting` class instance accessible via `chart.exporting`.

# What Changed

**Class Structure**
- Created `Exporting` class to encapsulate all exporting functionality
- Chart now has `chart.exporting` property containing the Exporting instance
- Applied same pattern to ExportData and OfflineExporting modules

**Method Migration**
Moved from `Chart.prototype` to `Exporting.prototype`:
- `exportChart()` → `chart.exporting.exportChart()`
- `getSVG()` → `chart.exporting.getSVG()`
- `print()` → `chart.exporting.print()`
- `getCSV()` → `chart.exporting.getCSV()`
- `getDataRows()` → `chart.exporting.getDataRows()`
- `getTable()` → `chart.exporting.getTable()`
- `viewData()` / `hideData()` → `chart.exporting.viewData()` / `hideData()`
- ... and more

**Property Updates**
- `chart.exportSVGElements` → `chart.exporting.svgElements`
- `chart.exportDivElements` → `chart.exporting.divElements`
- `chart.exportContextMenu` → `chart.exporting.contextMenuEl`
- `chart.exportingGroup` → `chart.exporting.group`
- `chart.dataTableDiv` → `chart.exporting.dataTableDiv`
- `chart.isPrinting` → `chart.exporting.isPrinting`
- etc.

**Backward Compatibility**
- Added deprecation wrappers on Chart.prototype for all moved methods
- Old API still functional but marked as `@deprecated`

**Updates**
- ~30 samples/demos updated to new API
- ~50 unit tests updated to new API
- Documentation updated with new paths

# Migration Example

```js
// Before
chart.exportChart(options);
chart.getSVG();
chart.print();
const csv = chart.getCSV();
chart.viewData();

// After
chart.exporting.exportChart(options);
chart.exporting.getSVG();
chart.exporting.print();
const csv = chart.exporting.getCSV();
chart.exporting.viewData();

// Safe access
chart.exporting?.print();
```

# Benefits
- ✅ Cleaner separation of concerns
- ✅ Exporting logic isolated in dedicated class
- ✅ Easier to maintain and extend
- ✅ Better code organization
- ✅ Optional null-safety with `chart.exporting?` checks
- ✅ Backward compatible via wrappers