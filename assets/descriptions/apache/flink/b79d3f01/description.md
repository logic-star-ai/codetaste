# Title
-----
Refactor deprecated Configuration getter/setter methods to use generic `get()` and `set()`

# Summary
-------
Replace all usages of deprecated type-specific Configuration methods (`getXxx(ConfigOption<Xxx>)`, `getXxx(ConfigOption<Xxx>, Xxx)`, and `setXxx(ConfigOption<Xxx>, Xxx)`) with the generic `get()` and `set()` methods throughout the codebase.

# Why
---
Following FLINK-34080 which deprecated the type-specific Configuration methods, all call sites need to be migrated to use the recommended generic methods to:
- Eliminate deprecated API usage
- Use the modern Configuration API consistently across the codebase
- Prepare for eventual removal of deprecated methods

# Changes
---------
**Pattern replacements:**
- `configuration.getString(option)` → `configuration.get(option)`
- `configuration.getInteger(option)` → `configuration.get(option)`
- `configuration.getLong(option)` → `configuration.get(option)`
- `configuration.getBoolean(option)` → `configuration.get(option)`
- `configuration.getFloat(option)` → `configuration.get(option)`
- `configuration.getDouble(option)` → `configuration.get(option)`
- `configuration.getXxx(option, default)` → `configuration.get(option, default)`
- `configuration.setString(option, value)` → `configuration.set(option, value)`
- `configuration.setInteger(option, value)` → `configuration.set(option, value)`
- ... (all type-specific setters)

**Scope:**
- flink-clients/...
- flink-connectors/...
- flink-core/...
- flink-external-resources/...
- flink-filesystems/...
- flink-formats/...
- flink-kubernetes/...
- flink-runtime/...
- flink-streaming-java/...
- flink-table/...
- flink-tests/...
- flink-yarn/...