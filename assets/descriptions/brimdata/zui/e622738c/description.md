# Refactor State Management to Use Snapshot Model

## Summary
Replace query version slice of state with a unified snapshot model. Reorganize session page to use snapshot-based routing with URL containing snapshot ID to populate editor and pins.

## Changes

### New Snapshot Model
Introduce `Snapshot` entity with schema:
- `id` - unique identifier
- `value` - query text
- `pins` - query pins array  
- `queryId` - reference to named query (nullable)
- `sessionId` - reference to session

### Routing
- Session page requires `snapshot.id` in URL (`/snapshots/:id`)
- Navigate to snapshots instead of query versions
- Update tab histories to use snapshot paths

### State Cleanup
Remove deprecated state slices:
- ~~`queryVersions`~~ 
- ~~`sessionQueries`~~
- ~~`sessionHistories`~~

Replace with:
- `snapshots` - EntityState of all snapshots

### Model Refactoring
- ~~`EditorSnapshot` class~~ → `Snapshot` entity
- ~~`QueryModel`~~ → Simplified query handling
- ~~`ActiveQuery`~~ → Use snapshot directly
- Snapshots now first-class citizens with own ID/lifecycle

### Benefits
- Simpler mental model - one concept instead of queries+versions
- Easier global history implementation
- Clearer ownership: snapshots belong to sessions AND queries
- Reduced indirection in state tree
- Simplified navigation logic

## Implementation Notes
- Migration `202409271055_migrateToSnapshots` handles state upgrade
- History now list of snapshots (reverse chronological)
- Query sessions create/navigate snapshots directly
- Named queries store latest content in query record itself