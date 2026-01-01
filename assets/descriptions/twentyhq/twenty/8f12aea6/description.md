# Refactor EntityBoard to RecordBoard

## Summary
Rename board components from `EntityBoard*` to `RecordBoard*` and reorganize module structure to align with `RecordTable` naming conventions.

## Why
Consistency with the established `RecordTable` pattern introduced earlier. The board functionality should follow the same naming scheme for better code organization and developer understanding.

## Changes

### Renaming
- `EntityBoard` → `RecordBoard`
- `EntityBoardColumn` → `RecordBoardColumn`
- `EntityBoardCard` → `RecordBoardCard`
- `EntityBoardActionBar` → `RecordBoardActionBar`
- `EntityBoardContextMenu` → `RecordBoardContextMenu`
- `BoardColumnMenu` → `RecordBoardColumnDropdownMenu`
- `BoardColumnEditTitleMenu` → `RecordBoardColumnEditTitleMenu`

### File Organization
- Move `ui/layout/board/*` → `ui/object/record-board/*`
- Reorganize into subfolders:
  - `action-bar/`
  - `context-menu/`
  - `options/`
  - `components/`
  - `hooks/`
  - `states/`
  - `types/`

### Code Consolidation
- Merge `BoardColumn` + `EntityBoardColumn` → single `RecordBoardColumn` component
- Inline `StyledBoard` component
- Remove unnecessary exports
- Update all import paths across the codebase

## Scope
All board-related components, hooks, states, and types. Update imports in companies module, opportunities pages, and view utilities.