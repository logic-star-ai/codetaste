# Complete `uint256` to `Txid`/`Wtxid` type safety conversion

Convert all remaining `uint256` usage to strongly-typed `Txid`/`Wtxid` throughout the codebase. Move `transaction_identifier.h` to `primitives/` and remove implicit conversions to enforce type safety.