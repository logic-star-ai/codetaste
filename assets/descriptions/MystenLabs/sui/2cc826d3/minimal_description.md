# Extract JSON-RPC API definitions into separate `sui-json-rpc-api` crate

Create new `sui-json-rpc-api` crate and move all RPC API trait definitions from `sui-json-rpc/src/apis/*` into it. Update `sui-sdk` to depend only on `sui-json-rpc-api` instead of `sui-json-rpc`.