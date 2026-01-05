# Title

Rename `TableRule` to `ShardingTable` for improved module identification

## Summary

Refactor `TableRule` class to `ShardingTable` throughout the codebase to enhance naming clarity and module boundary identification in the sharding feature.

## Why

The name `TableRule` is too generic and doesn't clearly indicate its association with sharding functionality. Adding the "Sharding" prefix:
- Improves code readability
- Makes module boundaries more explicit
- Aligns with naming conventions used elsewhere in the sharding module

## Changes

**Class Rename:**
- `TableRule` → `ShardingTable`
- File: `TableRule.java` → `ShardingTable.java`

**Method Renames:**
- `findTableRule()` → `findShardingTable()`
- `getTableRule()` → `getShardingTable()`
- `findTableRuleByActualTable()` → `findShardingTableByActualTable()`
- `getTableRules()` → `getShardingTables()`

**Collection Renames:**
- `Map<String, TableRule> tableRules` → `Map<String, ShardingTable> shardingTables`

**Affected Modules:**
- `features/sharding/core/` - Core sharding logic (auditor, cache, decider, merge, metadata, route, rule, etc.)
- `features/sharding/distsql/handler/` - DistSQL query handlers and checkers
- `kernel/data-pipeline/scenario/cdc/` - CDC pipeline utilities
- All corresponding test files

**Note:** Pure refactoring with no functional changes.