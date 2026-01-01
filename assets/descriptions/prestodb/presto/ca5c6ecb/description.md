Title
-----
Refactor: Push Split abstraction to SPI and eliminate PartitionChunk

Summary
-------
Moved `Split` interface from internal `presto-main` to public `presto-spi` layer and removed `PartitionChunk` interface, consolidating on `Split` as the unified abstraction for work distribution.

Why
---
- `Split` is a fundamental concept that connectors need to implement
- Having both `PartitionChunk` and `Split` created unnecessary duplication
- Split belongs in SPI as a core plugin interface concept

Changes
-------

**API Changes:**
- Moved `Split` interface to `presto-spi` package
- Moved `HostAddress` to `presto-spi` package  
- Removed `PartitionChunk` interface entirely
- Added `PartitionedSplit` interface to SPI
- Renamed `ImportClient.getPartitionChunks()` → `getPartitionSplits()`
- Removed `ImportClient.serializePartitionChunk()` / `deserializePartitionChunk()`
- Added `canHandle(Split)` to `ConnectorHandleResolver` and `ImportClient`
- Added `getSplitClass()` to handle resolvers

**Hive Connector:**
- Renamed `HivePartitionChunk` → `HiveSplit`
- Removed `HiveChunkEncoder` (serialization no longer needed)
- Renamed internal iterators/queues from "chunk" to "split"
- Updated schema parameter naming: `chunkSchema` → `splitSchema`

**Configuration:**
- Renamed all config properties: `max-chunk-*` → `max-split-*`
- Added `@LegacyConfig` annotations for backward compatibility
- Examples: `hive.max-chunk-size` → `hive.max-split-size`

**Internal Changes:**
- Removed `ImportSplit` wrapper class
- Removed `DataSourceType` enum - now using polymorphic `canHandle()`
- Removed `SerializedPartitionChunk` 
- Updated `ConnectorDataStreamProvider` to work with `Split`
- Added split-specific handle resolvers: `RemoteSplitHandleResolver`, `CollocatedSplitHandleResolver`
- Added `SplitJacksonModule` for JSON serialization

**Terminology:**
- Consistently renamed "chunk" → "split" throughout codebase
- Updated class names, method names, variable names, comments

Migration Notes
---------------
- Plugins implementing `ImportClient` must update method signatures
- Configuration files should migrate to new property names (legacy names supported)
- Any code referencing `PartitionChunk` must be updated to use `Split`