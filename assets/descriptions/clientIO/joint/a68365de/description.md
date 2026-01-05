# Refactor: Remove jQuery Dependency

## Summary

Remove jQuery as a runtime dependency and replace it with a custom internal DOM utility (~30kB unminified) that preserves event namespaces and delegation functionality while reducing bundle size and external dependencies.

## Why

- **Reduce dependencies**: Eliminate external dependency on jQuery
- **Smaller footprint**: Custom utility is significantly smaller than full jQuery
- **Modernization**: Native browser APIs now provide much of what jQuery offered
- **More control**: Internal implementation allows for tailored functionality
- **WeakMap storage**: Uses WeakMap instead of hidden DOM properties for data storage

## What Changed

- Created internal DOM utility for event handling (namespaces + delegation)
- jQuery preserved as `devDependency` only (used in docs/demos)
- Event system remains compatible with previous versions
- Data storage moved to WeakMap instead of element properties

## Breaking Changes

### Selector Support
- ❌ jQuery-specific selectors no longer supported
- ✅ Only CSS3 selectors recognized
- Removed: `:not=`, `:first`, `:eq()`, `:odd`, `:input`, `:checkbox`, `:animated`, `:visible`, `:hidden`, custom jQuery extensions, etc.

### View API Changes
- ❌ `view.$el` and `view.$()` removed (were public)
- ✅ Use `view.el` and `view.el.querySelectorAll()` instead

### Paper Properties
- ❌ Removed: `paper.$document`, `paper.$grid`, `paper.$background`

### Utilities
- `utils.sortElement` now returns plain `Element[]` (not jQuery object)

### Data Access
- ❌ Can no longer access CellView via `$.data(element)`

### Method Changes
- ❌ `cellView.prototype.findBySelector()` removed
- ✅ Use: `findNode()`, `findPortNode()`, `findLabelNode()`
- ✅ Group variants: `findNodes()`, `findPortNodes()`, `findLabelNodes()`

## Notes

- Watch for CSS style unit handling (jQuery auto-added units, e.g., `{width: 100}`)
- SVG attributes don't require units, but CSS styles may need adjustment