Title
-----
Replace `SessionOption(s)` with `ClientFactoryBuilder`

Summary
-------
Simplify `ClientFactory` construction by replacing the generic `SessionOption`/`SessionOptions` mechanism with a dedicated `ClientFactoryBuilder`. 

Why
---
`SessionOption(s)` was originally designed to support multiple protocols, but now that Armeria only supports HTTP, this abstraction adds unnecessary complexity. A builder pattern provides a more intuitive and type-safe API for constructing `ClientFactory` instances.

Modifications
-------------
- Remove `SessionOption`, `SessionOptions`, and `SessionOptionValue` classes
- Add new `ClientFactoryBuilder` class with fluent API for configuring:
  - Event loop settings (`eventLoopGroup()`, `useDaemonThreads()`, `numWorkers()`)
  - Connection settings (`connectTimeout()`, `socketOption()`)
  - SSL/TLS configuration (`sslContextCustomizer()`)
  - HTTP protocol settings (`useHttp2Preface()`, `useHttp1Pipelining()`)
  - Connection pooling (`idleTimeout()`, `connectionPoolListener()`)
  - Address resolution (`addressResolverGroupFactory()`)
- Replace `AllInOneClientFactory` with `DefaultClientFactory`
- Merge `NonDecoratingClientFactory` into `HttpClientFactory` and `DefaultClientFactory`
- Simplify `ClientFactoryProvider` interface:
  - Before: `newFactory(SessionOptions, Map<Class<?>, ClientFactory>)`
  - After: `newFactory(ClientFactory httpClientFactory)`
- Make `ClientFactory` implementations package-local (`HttpClientFactory`, `DefaultClientFactory`, `GrpcClientFactory`, `THttpClientFactory`)
- Add default configuration constants to `Flags`:
  - `defaultNumServerBosses()`, `defaultNumServerWorkers()`, `defaultNumClientWorkers()`
  - `defaultConnectTimeoutMillis()`, `defaultServerIdleTimeoutMillis()`, `defaultClientIdleTimeoutMillis()`
- Rename `DecoratingKeyedChannelPoolHandler` → `KeyedChannelPoolHandlerWrapper`
- Update all usages throughout codebase (tests, examples, docs)
- Standardize Javadoc for `*Builder.build()` and `*Builder.newDecorator()` methods

Result
------
Simpler, more discoverable API for constructing `ClientFactory` instances with better type safety and IDE support.