# Refactor RPC lib folder structure and naming conventions

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