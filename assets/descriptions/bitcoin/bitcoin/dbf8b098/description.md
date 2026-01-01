# Title
-----
Complete `uint256` to `Txid`/`Wtxid` type safety conversion

# Summary
-------
Convert all remaining `uint256` usage to strongly-typed `Txid`/`Wtxid` throughout the codebase. Move `transaction_identifier.h` to `primitives/` and remove implicit conversions to enforce type safety.

# Why
---
- Prevent bugs from mixing transaction IDs with other 256-bit hashes
- Make code intent explicit (txid vs wtxid vs block hash vs ...)
- Type system catches errors at compile time rather than runtime

# Changes
-------
**Core Infrastructure:**
- Move `transaction_identifier.h` from `util/` to `primitives/`
- Remove implicit `uint256` conversion operators from `transaction_identifier` class
- Remove `uint256` comparison operators (force explicit conversions via `ToUint256()`)

**Mempool & Policy:**
- Convert `CTxMemPool` methods to accept `Txid` instead of `uint256`
  - `PrioritiseTransaction()`, `ApplyDelta()`, `ClearPrioritisation()` 
  - `GetTransactionAncestry()`, `GatherClusters()`, `GetIterVec()`
  - Internal maps and sets now use `Txid` keys
- Update `mapDeltas`, `m_unbroadcast_txids`, disconnected transactions tracking
- Convert RBF validation helpers to use `Txid` parameters
- Update fee estimator to use `Txid` internally

**Block & Merkle:**
- `CPartialMerkleTree` methods now work with `std::vector<Txid>`
- `CMerkleBlock::vMatchedTxn` now `std::vector<std::pair<unsigned int, Txid>>`
- Merkle root calculation functions convert via `.ToUint256()` only when needed

**RPCs:**
- Convert RPC handlers: `getmempoolancestors`, `getmempooldescendants`, `getmempoolentry`, `prioritisetransaction`, `getrawtransaction`, etc.
- Parse transaction ID parameters directly to `Txid` type

**Indexes & Storage:**
- `TxIndex` internally uses `Txid` for lookups
- Update `FindTx()`, `GetTransaction()` signatures

**Net Processing:**
- Update transaction download/relay to use `Txid`/`Wtxid` explicitly
- Convert announcement tracking, orphan handling

**Wallet:**
- Update wallet interfaces to accept `Txid` instead of `uint256`
- Convert spend/receive functions

**Tests:**
- Add `operator<<` overloads for `Txid`/`Wtxid` in test utilities
- Update all fuzz/unit tests

**Hashers:**
- Add dedicated `SaltedTxidHasher`, `SaltedWtxidHasher`, `SaltedUint256Hasher`
- Update containers to use appropriate hasher type