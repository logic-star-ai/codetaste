# Internal API cleanup

## Summary
Refactor internal APIs to reduce method proliferation on core interfaces and improve code organization by:
- Introducing context builder pattern
- Renaming/relocating classes for clarity
- Moving implementation details to internal packages
- Simplifying method names

## Changes

### Rename `HostnameResolver` → `NameResolver`
- Move from `io.vertx.core.impl` to `io.vertx.core.internal.resolver`
- Update `VertxInternal.hostnameResolver()` → `nameResolver()`
- Rename resolution methods: `resolveHostname()` → `resolve()`, `resolveHostnameAll()` → `resolveAll()`

### Introduce `ContextBuilder`
- Add `VertxInternal.contextBuilder()` returning fluent builder interface
- Builder methods: `withThreadingModel()`, `withEventLoop()`, `withClassLoader()`, `withCloseFuture()`, `withWorkerPool()`, `withDeploymentContext()`
- Remove multiple overloaded `createContext()` / `createEventLoopContext()` / `createWorkerContext()` / `createVirtualThreadContext()` methods
- Add `ContextInternal.toBuilder()` to create builder from existing context

### Simplify method names on `VertxInternal`
- `metricsSPI()` → `metrics()`
- `getEventLoopGroup()` → `eventLoopGroup()`
- `getAcceptorEventLoopGroup()` → `acceptorEventLoopGroup()`
- `getWorkerPool()` → `workerPool()`
- `getInternalWorkerPool()` → `internalWorkerPool()`
- `getClusterManager()` → `clusterManager()`
- Remove `resolveFile()` / `resolveAddress()` (use `fileResolver().resolve()` / `nameResolver().resolve()`)
- Remove `nettyAddressResolverGroup()` (use `nameResolver().nettyAddressResolverGroup()`)

### Move classes to internal packages
- `WorkerPool` → `io.vertx.core.internal`
- `WorkerExecutorInternal` → `io.vertx.core.internal`
- `DeploymentContext` → `io.vertx.core.internal.deployment`
- `ExecuteBlocking` (extracted from `WorkerPool`) → `io.vertx.core.impl`

### Other renames
- `FileResolver.resolveFile()` → `resolve()`
- `DeploymentContext.deploymentID()` → `id()`
- `WorkerExecutorInternal.getPool()` → `pool()`

### Type parameter for `AddressResolver`
- Add generic type parameter `<A extends Address>` for clarity
- Update `EndpointResolver` to use typed address parameter

## Why
- **Reduce API surface**: Fewer methods on core interfaces makes them easier to maintain and understand
- **Builder pattern**: Eliminates need for many overloaded context creation methods with different parameter combinations
- **Clearer naming**: Method names like `metrics()` vs `metricsSPI()` are more concise; `resolve()` is more intuitive
- **Better organization**: Moving implementation details to `internal` packages clarifies public vs internal APIs
- **Type safety**: Generic parameter on `AddressResolver` improves type clarity