Title
-----
Rename statistics classes to improve naming clarity

Summary
-------
Refactor statistics-related classes to use clearer, more concise naming conventions by:
- Removing `ShardingSphere` prefix from internal statistics classes
- Explicitly using `Statistics` suffix instead of `Data`
- Updating all related methods, fields, and accessors

Changes
-------
**Class Renamings:**
- `ShardingSphereDatabaseData` → `DatabaseStatistics`
- `ShardingSphereSchemaData` → `SchemaStatistics`
- `ShardingSphereTableData` → `TableStatistics`
- `ShardingSphereRowData` → `RowStatistics`

**Method/Field Updates:**
- `getDatabaseData()` → `getDatabaseStatisticsMap()`
- `getSchemaData()` → `getSchemaStatisticsMap()`
- `getTableData()` → `getTableStatisticsMap()`
- `containsDatabase()` → `containsDatabaseStatistics()`
- `putDatabase()` → `putDatabaseStatistics()`
- `dropDatabase()` → `dropDatabaseStatistics()`
- Similar updates for schema/table level methods...

**Service/Swapper Classes:**
- `ShardingSphereDataPersistService` → `ShardingSphereStatisticsPersistService`
- `YamlShardingSphereRowDataSwapper` → `YamlShardingSphereRowStatisticsSwapper`
- `YamlShardingSphereTableDataSwapper` → `YamlShardingSphereTableStatisticsSwapper`

**Utility Methods:**
- `assembleTableData()` → `assembleTableStatistics()`

**Manager Methods:**
- `addShardingSphereDatabaseData()` → `addDatabaseStatistics()`
- `dropShardingSphereDatabaseData()` → `dropDatabaseStatistics()`
- ... (schema/table variants)

Why
---
- Reduce naming verbosity by dropping `ShardingSphere` prefix from internal classes
- Clarify intent: these are **statistics** objects, not generic data containers
- Improve consistency across the codebase
- Better align with the actual purpose of these classes

Scope
-----
- All statistics domain classes in `infra.metadata.statistics` package
- Persist services, managers, swappers, collectors
- Test classes and fixtures
- SQL federation executor integrations
- Mode metadata management components