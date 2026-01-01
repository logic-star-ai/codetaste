# Title

Add RuleIdentifier to decouple ShardingSphere Rule architecture

# Summary

Refactor the ShardingSphere rule system from an inheritance-based design to a composition-based approach using the `RuleIdentifier` pattern. This removes the tight coupling between rules and their capabilities by introducing a unified `RuleIdentifiers` container that holds rule-specific identifiers.

# Why

- **Eliminate complex inheritance hierarchies**: Remove marker interfaces like `DataNodeContainedRule`, `TableMapperContainedRule`, and `DataSourceMapperContainedRule` that force rules into rigid inheritance structures
- **Improve extensibility**: Enable rules to declare capabilities through composition rather than interface implementation
- **Reduce coupling**: Decouple rule consumers from concrete rule types by querying for specific identifier capabilities
- **Simplify type checking**: Replace `instanceof` checks and casting with explicit identifier lookup patterns

# What Changed

**Removed Interfaces:**
- `DataNodeContainedRule` → Deleted
- `TableMapperContainedRule` → Deleted  
- `DataSourceMapperContainedRule` → Deleted

**New Components:**
- `RuleIdentifier` interface → Marker interface for all identifiers
- `RuleIdentifiers` class → Container holding multiple `RuleIdentifier` instances with `findIdentifier(Class)` and `getIdentifier(Class)` methods

**Modified Interfaces:**
- `DataNodeRule`, `DataSourceMapperRule`, `StaticDataSourceRule`, `TableMapperRule` → Now extend `RuleIdentifier`

**All ShardingSphereRule implementations:**
- Added `getRuleIdentifiers()` method returning `RuleIdentifiers` instance
- Rules now compose identifiers: `new RuleIdentifiers(dataNodeRule, tableMapperRule, ...)`

**Access Pattern Migration:**
```java
// Before
if (rule instanceof DataNodeContainedRule) {
    DataNodeRule dataNodeRule = ((DataNodeContainedRule) rule).getDataNodeRule();
}

// After  
Optional<DataNodeRule> dataNodeRule = rule.getRuleIdentifiers().findIdentifier(DataNodeRule.class);
if (dataNodeRule.isPresent()) { ... }
```

# Scope

**Core Changes:**
- `infra/common` → Rule infrastructure and identifier types
- `features/*` → BroadcastRule, EncryptRule, MaskRule, ReadwriteSplittingRule, ShadowRule, ShardingRule
- `kernel/single` → SingleRule
- All rule implementations across `kernel/*`

**Consumer Updates:**
- `jdbc/` → Metadata, result sets, statement execution
- `proxy/backend/` → Connector, handlers, response builders
- `infra/binder`, `infra/merge`, `infra/route` → Rule querying patterns
- `distsql/handler` → Rule checkers and executors

**Test Updates:**
- 50+ test files updated with new mocking patterns
- Test fixtures updated to implement `getRuleIdentifiers()`

# Impact

- ✅ No behavioral changes to end users
- ✅ Internal API refactoring only
- ⚠️ Breaking change for custom rule implementations (must implement `getRuleIdentifiers()`)
- ⚠️ All `findRules(XxxContainedRule.class)` calls replaced with identifier queries