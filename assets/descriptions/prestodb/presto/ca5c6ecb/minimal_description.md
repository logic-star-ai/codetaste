# Refactor: Push Split abstraction to SPI and eliminate PartitionChunk

Moved `Split` interface from internal `presto-main` to public `presto-spi` layer and removed `PartitionChunk` interface, consolidating on `Split` as the unified abstraction for work distribution.