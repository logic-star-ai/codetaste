Title
-----
Migrate RLP to alloy-rlp

Summary
-------
Replace internal `reth_rlp` implementation with `alloy_rlp = "0.3"` crate.

Why
---
- Remove maintenance burden of internal RLP crate
- Leverage battle-tested external implementation
- Align with alloy ecosystem

Changes
-------
- Remove `crates/rlp/` and `crates/rlp/rlp-derive/` directories
- Replace workspace dependency: `reth-rlp` → `alloy-rlp = "0.3"`
- Update imports throughout codebase: `reth_rlp::*` → `alloy_rlp::*`
- Replace `DecodeError` → `alloy_rlp::Error` or `alloy_rlp::Result`
- Replace `reth_rlp_derive::*` → `alloy_rlp` with `"derive"` feature
- Update error handling: `reth_rlp::DecodeError` → `alloy_rlp::Error`

Breaking Changes
----------------
- `DecodeError` type deprecated in favor of `alloy_rlp::Error`
- Global encode function generics order changed
- Error variants updated in types using RLP (e.g., `EthStreamError`, `PayloadError`, etc.)