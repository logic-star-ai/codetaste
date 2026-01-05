# Rename `crypto.Sha3{,Hash}()` to `crypto.Keccak256{,Hash}()`

## Summary
Rename all occurrences of `crypto.Sha3()` and `crypto.Sha3Hash()` to `crypto.Keccak256()` and `crypto.Keccak256Hash()` throughout the codebase.

## Why
Ethereum uses **Keccak-256**, not the standardized SHA-3. The current naming is misleading and suggests we're using the finalized SHA-3 standard, when we're actually using the original Keccak-256 algorithm (the SHA-3 competition submission before final standardization).

The standardized SHA-3 differs from Keccak-256 in padding, so the distinction matters for accuracy and clarity.

## Changes Required
- Rename `crypto.Sha3()` → `crypto.Keccak256()`
- Rename `crypto.Sha3Hash()` → `crypto.Keccak256Hash()`
- Update all call sites across:
  - `accounts/abi/...`
  - `common/...`
  - `core/...`
  - `crypto/...`
  - `eth/...`
  - `light/...`
  - `node/...`
  - `p2p/...`
  - `tests/...`
  - `trie/...`
  - `whisper/...`
- Update tests accordingly
- Update variable names (e.g., `emptyCodeHash`, `sha3_nil`) to use new function names
- Update comments referencing SHA-3 to mention Keccak-256 explicitly