# Title
Refactor database table view to decouple rendering from model

## Summary
Decouple database table rendering from the model layer by introducing a `TableViewManager` abstraction. This allows any data source implementing the interface to be rendered as a table, improving modularity and separation of concerns.

## Changes

### Selection System Unification
- Replace separate row-level and cell-level selection managers with unified `DatabaseSelection` system
- Introduce `DatabaseSelectionView` component handling all selection rendering and interactions
- Consolidate `DatabaseTableViewRowSelection` and `DatabaseTableViewCellSelect` into single `DatabaseSelection` type with `CellFocus` and `MultiSelection` 
- Remove `RowSelectionManager` and `CellSelectionManager` classes
- Simplify keyboard navigation and selection state management

### Table View Manager Abstraction  
- Create `TableViewManager` interface defining contract for renderable data sources
- Implement `DatabaseTableViewManager` to manage rows, columns, filtering, and view operations
- Extract view logic from `DatabaseBlockModel` into manager layer
- Enable any conforming data source to be rendered as table view

### Column Management Refactoring
- Introduce `ColumnManager` interface/classes encapsulating column behavior and data access
- Implement `DatabaseColumnManager` and `DatabaseTitleColumnManager`
- Move column rendering, width adjustment, and data updates to manager layer
- Columns now handle their own operations (rename, delete, duplicate, type changes, etc.)

### Position-Based Column Operations
- Replace index-based column insertion with `InsertPosition` type (start/end/before/after)
- Add `insertPositionToIndex()` utility for position resolution
- Update `addColumn()`, `moveColumn()`, and related methods to use positions
- Simplify column reordering logic

### Column Interaction Improvements
- Refactor column width adjustment with `ColumnWidthDragBar` component
- Simplify column drag-and-drop implementation
- Remove complex preview/indicator components (`ColumnDragPreview`, `ColumnDragIndicator`)
- Consolidate column header rendering in `DatabaseHeaderColumn` component
- Add drag utilities (`startDrag()`, `startFrameLoop()`)

### Cell Container Simplification
- Remove direct `DatabaseBlockModel` dependency from cell containers
- Use `ColumnManager` for all cell operations
- Simplify value get/set through manager methods
- Improve editing state handling

### API Cleanup
- Remove `moveColumn()` from model (now in view manager)
- Consolidate column update methods (`updateColumn()` now uses updater function)
- Remove `DatabaseTableViewRowStateType` and related types
- Clean up service slots (single `databaseSelectionUpdated` slot)

## Why
- **Separation of Concerns**: View logic separated from data model
- **Extensibility**: Any data source can now be rendered as table
- **Maintainability**: Simplified selection and interaction handling  
- **Testability**: Manager abstractions easier to test in isolation
- **Type Safety**: Cleaner type definitions with fewer union types