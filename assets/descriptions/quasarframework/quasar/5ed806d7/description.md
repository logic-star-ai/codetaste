# Reorganize component folder structure

## Summary

Refactor component directory structure to give each component its own dedicated folder instead of grouping related components together in category-based folders.

## Why

Current structure groups components by category (e.g., `/btn/`, `/datetime/`, `/list/`), which:
- Makes component boundaries less clear
- Creates inconsistent import patterns
- Complicates component isolation

Individual folders provide:
- Clearer component ownership
- Consistent import paths
- Easier navigation/maintenance
- Better component-based architecture alignment

## Changes

**Button components** → separate folders:
- `QBtnDropdown`: `/btn/` → `/btn-dropdown/`
- `QBtnGroup`: `/btn/` → `/btn-group/`
- `QBtnToggle`: `/btn/` → `/btn-toggle/`

**DateTime components** split:
- `QDate`: `/datetime/` → `/date/`
- `QTime`: `/datetime/` → `/time/`

**List components** reorganized:
- `QList`, `QItem`, `QItemSection`, `QItemLabel`: `/list/` → `/item/`
- `QExpansionItem`: `/list/` → `/expansion-item/`
- `QSlideItem`: `/list/` → `/slide-item/`

**Observer components** separated:
- `QResizeObserver`: `/observer/` → `/resize-observer/`
- `QScrollObserver`: `/observer/` → `/scroll-observer/`

**Table component** extracted:
- `QMarkupTable`: `/table/` → `/markup-table/`

**Mixins** consolidated to `/mixins/`:
- `btn-mixin.js` → `/mixins/btn.js`
- `datetime-mixin.js` → `/mixins/datetime.js`

**Update all references**:
- Import paths in component files
- Export paths in `components.js`
- CSS/SASS imports in `index.sass` & `index.styl`
- Create `index.js` for each component folder