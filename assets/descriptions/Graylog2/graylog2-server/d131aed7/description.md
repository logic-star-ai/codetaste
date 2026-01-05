# Add custom MongoDB interface for entity collections

## Summary
Introduce custom `MongoCollection` interface to wrap MongoDB driver's `MongoCollection` for entities implementing `MongoEntity`. This provides better control over data modification operations and enforces type constraints at the API level.

## Changes
- Add `org.graylog2.database.MongoCollection<T extends MongoEntity>` interface mirroring MongoDB driver methods
- Implement `MongoEntityCollection<T>` as wrapper around `com.mongodb.client.MongoCollection<T>`
- Replace `com.mongodb.client.MongoCollection` imports with custom interface throughout codebase (~50 files)
- Move `getOrCreate()` from `MongoUtils` to `MongoCollection` interface for better encapsulation
- Rename `MongoCollections#get()` → `nonEntityCollection()` for clarity on non-entity collections
- Add `MongoCollections#indexUtils()` to retrieve index tools for collections
- Remove `MongoCollection#getCollectionName()` (use `#getNamespace()` instead)

## Why
- Need more control over `MongoCollection` methods that modify data
- Enforce type constraints for `MongoEntity`-based documents at API level
- Better encapsulation of entity-specific operations (e.g., `getOrCreate()`)
- Clearer separation between entity and non-entity collections
- Improved type safety and consistency across MongoDB operations

## Technical Details
- Custom interface provides subset of MongoDB driver methods with `MongoEntity` constraint
- `MongoEntityCollection` delegates to underlying `com.mongodb.client.MongoCollection`
- `getOrCreate()` uses `findOneAndUpdate` with `$setOnInsert` for atomic get-or-create
- Added comprehensive Javadoc mirroring MongoDB driver documentation
- Uses `@Nonnull`/`@Nullable` annotations for null-safety

## Testing
- Add `MongoEntityCollectionTest` for `getOrCreate()` behavior
- Move relevant tests from `MongoUtilsTest` to new collection tests
- Verify null handling and atomicity of operations