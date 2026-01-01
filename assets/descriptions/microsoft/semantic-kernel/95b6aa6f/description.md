# Rename VectorStoreProperty and attribute members for clarity and brevity

## Summary
Rename properties on `VectorStoreProperty` class and related attributes to use shorter, clearer names:
- `DataModelPropertyName` → `Name`
- `StoragePropertyName` → `StorageName`
- `PropertyType` → `Type`

## Why
Current naming is verbose and inconsistent. The new names:
- Reduce verbosity (`DataModelPropertyName` is unnecessarily long)
- Improve clarity (`Name` is intuitive for the property name on the data model)
- Better align with .NET conventions (`Type` is more idiomatic than `PropertyType`)

## Changes

### VectorStoreProperty (base class)
- ~~`DataModelPropertyName`~~ → **`Name`**
- ~~`StoragePropertyName`~~ → **`StorageName`**
- ~~`PropertyType`~~ → **`Type`**

### Attributes
Apply same changes to:
- `VectorStoreKeyAttribute`
- `VectorStoreDataAttribute`
- `VectorStoreVectorAttribute`

### Affected classes
- `VectorStoreKeyProperty`
- `VectorStoreDataProperty`
- `VectorStoreVectorProperty`
- `VectorStoreVectorProperty<TInput>`

## Scope
Update all references throughout:
- Core abstractions
- All connectors (AzureAISearch, CosmosMongoDB, CosmosNoSql, MongoDB, PgVector, Qdrant, Redis, SqliteVec, Weaviate, SqlServer)
- Samples
- Unit tests
- Integration tests