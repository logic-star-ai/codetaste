# Remove LazyBlock

## Summary
Remove `LazyBlock` implementation and related lazy loading infrastructure from the SPI. The new `SourcePage` interface makes lazy blocks obsolete.

## Why
With the introduction of `SourcePage`, lazy materialization of column data is now handled at the page source level rather than at the block level. This eliminates the need for `LazyBlock` wrapping and simplifies the block hierarchy.

## What's Removed

### SPI Classes
- `LazyBlock`
- `LazyBlockEncoding` 
- `LazyBlockLoader` interface

### Block Methods
- `Block.isLoaded()`
- `Block.getLoadedBlock()`
- `ArrayBlock.isLoaded()` / `ArrayBlock.getLoadedBlock()`
- `MapBlock.isLoaded()` / `MapBlock.getLoadedBlock()`
- `RowBlock.isLoaded()` / `RowBlock.getLoadedBlock()`
- `RunLengthEncodedBlock.isLoaded()` / `RunLengthEncodedBlock.getLoadedBlock()`
- `DictionaryBlock.isLoaded()` / `DictionaryBlock.getLoadedBlock()`

### Page Methods
- `Page.getLoadedPage()`
- `Page.getLoadedPage(int)`
- `Page.getLoadedPage(int[])`
- `Page.getLoadedPage(int[], int[])`

## Changes Required

**BlockEncodingManager**: Remove `LazyBlockEncoding` registration

**Operators**: Remove calls to `.getLoadedBlock()` / `.getLoadedPage()` throughout:
- `JoinProbe`, `JoinDomainBuilder`, `StreamingAggregationOperator`
- `TableScanOperator`, `WorkProcessorSourceOperatorAdapter`
- `GroupedAggregator`, `InMemoryHashAggregationBuilder`
- `LookupJoinPageBuilder`, `PageProcessor`
- ...

**Page Sources**: Remove eager loading logic in ORC/Parquet readers

**Projections**: Simplify `DictionaryAwarePageProjection` - no lazy block handling needed

**Tests**: Remove tests for lazy block behavior

**Utility Methods**: Remove `BlockUtil.ensureBlocksAreLoaded()`, `PageChannelSelector.identitySelection()`, etc.