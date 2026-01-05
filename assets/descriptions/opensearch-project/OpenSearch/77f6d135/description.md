# Title

Refactor remaining `ImmutableOpenMap` usage to `java.util.Map` and remove class

# Summary

Replace all remaining occurrences of HPPC-backed `ImmutableOpenMap<K, V>` with standard `java.util.Map<K, V>` and completely remove the `ImmutableOpenMap` class from the codebase.

# Why

- Eliminate dependency on HPPC (High Performance Primitive Collections) for non-primitive types
- Standardize on Java collections API for better maintainability and familiarity
- Reduce custom collection abstractions in favor of standard library implementations
- Final cleanup to complete migration away from `ImmutableOpenMap`

# Scope

**Core Classes to Update:**
- `DiscoveryNodes` - cluster node maps (data nodes, master/cluster-manager nodes, ingest nodes, etc.)
- `GetIndexResponse` / `GetSettingsResponse` - index metadata retrieval
- `IndicesShardStoresResponse` - shard store status maps
- `StreamInput` / `StreamOutput` - remove `ImmutableOpenMap` serialization methods

**Patterns to Replace:**
- `ImmutableOpenMap.Builder` → `HashMap` + `Collections.unmodifiableMap()`
- `.valuesIt()` / `.keysIt()` → `.values().iterator()` / `.keySet().iterator()`
- `cursor.value` / `cursor.key` → `entry.getValue()` / `entry.getKey()`
- `.toArray(Type.class)` → `.toArray(new Type[0])`
- `ObjectCursor` / `ObjectObjectCursor` iterations → standard for-each loops

**Areas Affected:**
- Cluster state management and routing
- Index/shard allocation logic
- Admin APIs (get index, get settings, shard stores)
- Ingest node selection
- Test utilities and assertions

**Removals:**
- `ImmutableOpenMap` class and builder
- `CollectionAssertions.hasKey()` / `hasAllKeys()` test helpers
- `AbstractResponseTestCase.assertMapEquals()` utility

# Implementation Notes

- Use `Collections.unmodifiableMap()` to maintain immutability guarantees
- Ensure proper null-safety when converting collections
- Update all serialization code to use standard map read/write methods
- Replace HPPC cursor iterations with Java 8+ stream/iterator patterns where appropriate