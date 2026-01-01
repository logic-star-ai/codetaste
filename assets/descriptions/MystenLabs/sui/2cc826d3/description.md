# Extract JSON-RPC API definitions into separate `sui-json-rpc-api` crate

## Summary
Create new `sui-json-rpc-api` crate and move all RPC API trait definitions from `sui-json-rpc/src/apis/*` into it. Update `sui-sdk` to depend only on `sui-json-rpc-api` instead of `sui-json-rpc`.

## Why
Currently `sui-sdk` depends on `sui-json-rpc`, which transitively pulls in `sui-core` and numerous heavy dependencies. This forces anyone developing with `sui-sdk` to compile most of the sui repo.

By extracting API traits/interfaces into a lightweight crate, `sui-sdk` can avoid the heavy dependency chain while still accessing the API definitions it needs.

## Changes

**New crate:**
- `crates/sui-json-rpc-api/` with minimal dependencies

**Move from `sui-json-rpc/src/api/` to `sui-json-rpc-api/src/`:**
- `coin.rs` → API traits for coin operations
- `extended.rs` → Extended API traits
- `governance.rs` → Governance API traits
- `indexer.rs` → Indexer API traits
- `move_utils.rs` → Move utils API traits
- `read.rs` → Read API traits
- `transaction_builder.rs` → Transaction builder API traits
- `write.rs` → Write API traits
- Constants: `CLIENT_SDK_TYPE_HEADER`, `CLIENT_TARGET_API_VERSION_HEADER`, etc.

**Update dependencies:**
- `sui-sdk`: remove `sui-json-rpc` dependency, add `sui-json-rpc-api`
- All other crates: update imports from `sui_json_rpc::api::*` → `sui_json_rpc_api::*`

**Keep `sui-json-rpc-api` lean:**
- Only essential dependencies: `jsonrpsee`, `sui-types`, `sui-json-rpc-types`, etc.
- No `sui-core`, no heavy infrastructure crates

## Result
`sui-sdk` remains lightweight and suitable for external development without forcing compilation of the entire sui node infrastructure.