Title
-----
Refactor RPC lib folder structure and naming conventions

Summary
-------
Reorganize `rpc/lib/` to `rpc/jsonrpc/` and rename packages/types/functions to follow Go naming conventions and improve clarity.

**Directory changes:**
- Move `lib/` → `jsonrpc/`

**Package renames:**
- `rpc` → `jsonrpc`
- `rpcclient` → `client`  
- `rpcserver` → `server`

**Type renames:**
- `JSONRPCClient` → `Client`
- `JSONRPCRequestBatch` → `RequestBatch`
- `JSONRPCCaller` → `Caller`

**Function renames:**
- `StartHTTPServer` → `Serve`
- `StartHTTPAndTLSServer` → `ServeTLS`
- `NewURIClient` → `NewURI`
- `NewJSONRPCClient` → `New`
- `NewJSONRPCClientWithHTTPClient` → `NewWithHTTPClient`
- `NewWSClient` → `NewWS`

**Cleanup:**
- Unexpose `ResponseWriterWrapper` → `responseWriterWrapper`
- Remove unused `http_params.go`

Why
---
- Current `lib/` folder name is too generic and doesn't convey purpose
- `JSONRPC` prefix on types is redundant when already in `jsonrpc` package
- Function names like `StartHTTPServer` are verbose compared to idiomatic `Serve`
- Package structure doesn't follow Go conventions
- `ResponseWriterWrapper` shouldn't be part of public API
- Dead code (`http_params.go`) should be removed

Impact
------
**Breaking change** - updates all imports and function calls across codebase

Closes #3857