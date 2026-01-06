# Split Supports.{cpp,h} into Metal/Wooden and refactor wooden support mappings

Split monolithic `Supports.{cpp,h}` (1581 lines) into separate `MetalSupports` and `WoodenSupports` files. Refactor wooden support data structures to use direct array indexing instead of conditional lookups.