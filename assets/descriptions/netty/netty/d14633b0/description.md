Title
-----
Remove all Java 6/7 version checks and guards after Java 8 baseline bump

Summary
-------
Clean up codebase by removing all Java 6/7 compatibility code now that Java 8 is the minimum supported version for Netty 4.2. This includes:
- Removing runtime version checks (`PlatformDependent.javaVersion() >= 7/8`)
- Removing `@SuppressJava6Requirement` annotations
- Removing Java 6/7 fallback implementations
- Using Java 8+ APIs directly without guards

Why
---
Netty 4.2 now requires Java 8 as minimum version. Version guards and compatibility code for older JDKs are:
- No longer needed
- Add unnecessary complexity
- Make code harder to read/maintain
- Increase test surface without benefit

Scope
-----
**Modules affected:**
- `buffer/` - ByteBuf unsafe operations, allocation strategies
- `codec-http/` - WebSocket base64 encoding, SPDY compression
- `codec-http2/` - Exception handling
- `codec/` - Compression (zlib, deflate), checksum utilities
- `common/` - PlatformDependent utilities, NativeLibraryLoader, socket utils, thread-local random
- `handler/` - SSL/TLS context and engine implementations (JDK, OpenSSL, BouncyCastle, Conscrypt, Jetty ALPN)
- `resolver-dns/` - DNS caching, error handling
- `transport/` - NIO channels, selectors, exception handling
- `transport-native-unix-common/` - Unix channel utilities
- `transport-classes-epoll/` - Linux socket operations

**Key changes:**
- Remove conditional Java version checks
- Delete Java6/7-specific utility classes (Java7SslParametersUtils, Java8SslUtils, ThreadLocalRandom, ...)
- Use Java 8 APIs directly: `Base64`, `Files`, `ThreadLocalRandom`, `Deflater.SYNC_FLUSH`, `StandardProtocolFamily`, ...
- Update Animal Sniffer to enforce Java 8 baseline
- Deprecate `@SuppressJava6Requirement`, add `@SuppressJava8Requirement`
- Add Revapi ignores for annotation removals

**Testing:**
- Verify all version-guarded code paths still work correctly
- Ensure no behavioral regressions
- Confirm Animal Sniffer validation passes