# Remove Deprecated Java APIs

## Summary
Remove deprecated Java APIs that have been replaced with improved alternatives, cleaning up technical debt and reducing maintenance burden.

## Deprecated APIs to Remove

### Core Components
- **`WS` class** → Use injected `WSClient`
- **`CacheApi`** → Use `SyncCacheApi` or `AsyncCacheApi`
- **`Configuration` class** → Use Typesafe `Config` directly
- **`Play` global state access** → Use dependency injection
- **`Classpath` utilities** → No longer needed after Plugin API removal

### Request/Response APIs
- **`username()`/`withUsername()`** from `Request` → Use `Security.USERNAME` typed attribute
- **`tags()` from `RequestHeader`** → Use typed `attrs()`
- **`_underlyingHeader()`/`_underlyingRequest()`** → Use `asScala()`
- **Deprecated `Result` constructors** → Use updated signatures
- **`Results.*()` methods with String charset** → Use enum-based encoding
- **`Response.setContentType()`/`setCookie()` legacy methods** → Use builder pattern

### Testing APIs
- **`route(Call)`/`routeAndCall()` static methods** → Use application-scoped versions
- **`WithApplication.inject()`** → Use `instanceOf()`
- **Global state dependent test helpers** → Require explicit app parameter

### Concurrent APIs
- **`Timeout` interface** → Use `Futures` instead
- **`Futures.timeout()`/`delayed()` static methods** → Use injected instance
- **`HttpExecution.defaultContext()`** → Use injected `ExecutionContext`

### Forms & Data
- **`Form.data()`/`error()`/`reject()`** → Use getter methods and `withError()`
- **`DynamicForm` legacy methods** → Use updated API
- **`Formatters.parse()` with explicit class** → Type inference based version

### Security & Crypto
- **`CSRFTokenSigner.constantTimeEquals()`** → Use `MessageDigest.isEqual()`

### Application Loader
- **`Context.underlying()`/`initialConfiguration()`** → Use `asScala()`/`getConfig()`
- **`ApplicationLoader.Context.create()` static** → Use instance methods
- **`GuiceApplicationBuilder.loadConfig(Configuration)`** → Use `Config` version

### Other Components
- **`Environment.underlying()`** → Use `asScala()`
- **`MessagesApi.scalaApi()`** → Use `asScala()`
- **`Files.TemporaryFile.file()`** → Use `path()`
- **`ApplicationProvider.getApplication()`** → Use `get()`
- **`Router.Tags` constants** → Use `Router.Attrs.HANDLER_DEF`
- **`ConfigurationProvider`** → No replacement needed
- **Reflections-based scanning utilities** → No longer used

## Implementation Details
- Update binary compatibility filters to exclude removed deprecated APIs
- Update documentation links to point to correct classes/methods
- Ensure all tests use non-deprecated APIs
- Remove supporting deprecated classes like `RoutingDslProvider`, `ReflectionsCache`

## Why
These APIs were deprecated in earlier versions (mostly 2.5.x/2.6.0) and have well-established replacements. Removing them:
- Reduces maintenance burden
- Simplifies codebase
- Encourages modern patterns (DI, typed attributes, etc.)
- Eliminates global state dependencies
- Aligns with Scala 2.12+ and prepares for future versions