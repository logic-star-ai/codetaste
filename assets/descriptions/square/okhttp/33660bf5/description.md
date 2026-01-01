Title
-----
Rename FramedConnection to Http2Connection and HttpStream to HttpCodec

Summary
-------
Refactor internal HTTP implementation classes to use clearer, more descriptive names. Rename `FramedConnection` → `Http2Connection` and `HttpStream` → `HttpCodec` to better reflect their purposes.

Why
---
- `FramedConnection` name is ambiguous and doesn't clearly indicate HTTP/2 specificity
- `HttpStream` is misleading since it's actually an encoder/decoder interface, not a stream
- `HttpCodec` better represents the encode/decode functionality for both HTTP/1.1 and HTTP/2
- Improved naming makes codebase more maintainable and intention clearer

Changes
-------
**Core Renames:**
- `FramedConnection` → `Http2Connection`
- `HttpStream` → `HttpCodec`
- `Http1xStream` → `Http1Codec` 
- `Http2xStream` → `Http2Codec`
- `FramedStream` → `Http2Stream`
- `FrameReader` → `Http2Reader`
- `FrameWriter` → `Http2Writer`
- `FramedServer` → `Http2Server`

**Package Reorganization:**
- Move `okhttp3.internal.framed.*` → `okhttp3.internal.http2.*`
- Move `Http1xStream` → `okhttp3.internal.http1.Http1Codec`
- Consolidate HTTP/2 related classes under `internal.http2` package

**Variable/Field Updates:**
- `framedConnection` → `http2Connection`
- `httpStream` → `httpCodec`
- `frameWriter` → `writer`
- `frameReader` → `reader`

**Update References:**
- Update all usages in `StreamAllocation`, `ConnectInterceptor`, `CallServerInterceptor`, etc.
- Update test classes and mock implementations
- Update internal connection pooling and stream allocation logic