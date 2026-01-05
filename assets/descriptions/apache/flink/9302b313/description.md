# Remove deprecated Table API string expressions

## Summary
Remove deprecated string-based expression DSL from Table API across all language bindings (Java, Scala, Python). Replace with typed Expression API.

## Why
- String expressions were deprecated in favor of type-safe Expression DSL
- Reduces maintenance burden and complexity
- Eliminates parser infrastructure (`ExpressionParser`, `ExpressionParserFactory`)
- Improves compile-time type safety and IDE support

## Changes

### Core Removals
- `ExpressionParser` / `ExpressionParserFactory` classes
- `scala-parser-combinators` dependency
- All deprecated string-based method overloads in:
  - `Table` (select, filter, where, groupBy, orderBy, join*, addColumns, renameColumns, dropColumns, map, flatMap, aggregate, flatAggregate, ...)
  - `GroupedTable` (select, aggregate, flatAggregate)
  - `AggregatedTable` / `FlatAggregateTable` (select)
  - `WindowGroupedTable` (groupBy, select, aggregate, flatAggregate)
  - `GroupWindowedTable` (groupBy)
  - `OverWindowedTable` (select)

### Window API
- Remove string overloads from:
  - `Tumble.over(String)`, `TumbleWithSize.on(String)`
  - `Slide.over(String)`, `SlideWithSize.every(String)`, `SlideWithSizeAndSlide.on(String)`
  - `Session.withGap(String)`, `SessionWithGap.on(String)`
  - `Over.orderBy(String)`, `Over.partitionBy(String)`, `OverWindowPartitioned.orderBy(String)`, `OverWindowPartitionedOrdered.preceding(String)`

### StreamTableEnvironment
- `fromDataStream(DataStream, String)` 
- `registerDataStream(String, DataStream, String)`
- `createTemporaryView(String, DataStream, String)`

### Schema API
- String expression parameters in `Schema.Builder` methods

### Python API
- Remove string expression support throughout `pyflink.table`
- Update all tests/examples to use typed expressions (`col()`, `lit()`, `call()`, etc.)

### Test Updates
- ~50+ test files updated to use Expression DSL
- Remove all `stringexpr` test packages
- Update validation tests

## Migration
Users must migrate from:
```java
table.select("a, b, c").where("a > 5")
```

To:
```java
table.select($("a"), $("b"), $("c")).where($("a").isGreater(5))
```