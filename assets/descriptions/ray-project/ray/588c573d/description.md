# Title
-----
Refactor Java worker code structure: consolidate modules and reorganize packages

# Summary
-------
Refactor Java worker codebase to simplify module structure and improve package organization. Merge multiple modules into single `runtime` module, reorganize code into meaningful packages, and remove implicit reflection-based dependencies.

# Changes
---------

## Module Consolidation
- Merge `runtime-common`, `runtime-dev`, `runtime-native`, and `common` modules → single `runtime` module
- Eliminate implicit dependencies caused by reflection
- Simplify dependency management in pom.xml files

## Package Reorganization
- `org.ray.core.*` → `org.ray.runtime.*`
- `org.ray.spi.*` → domain-specific packages:
  - `org.ray.runtime.config` - RayParameters, RunMode, WorkerMode, PathConfig
  - `org.ray.runtime.functionmanager` - LocalFunctionManager, RemoteFunctionManager, RayMethod, ...
  - `org.ray.runtime.gcs` - KeyValueStoreLink, RedisClient, StateStoreProxy, ...
  - `org.ray.runtime.objectstore` - ObjectStoreProxy, MockObjectStore
  - `org.ray.runtime.raylet` - RayletClient, RayletClientImpl, MockRayletClient
  - `org.ray.runtime.task` - TaskSpec, FunctionArg, ArgumentsBuilder
  - `org.ray.runtime.runner` - RunManager, ProcessInfo, worker classes
  - `org.ray.runtime.generated` - Flatbuffer generated classes
- `org.ray.util.*` → `org.ray.runtime.util.*`

## Renames
- `LocalSchedulerLink` → `RayletClient`
- `DefaultLocalSchedulerClient` → `RayletClientImpl`
- `MockLocalScheduler` → `MockRayletClient`
- `org.ray.core.impl.RayDevRuntime` → `org.ray.runtime.RayDevRuntime`
- `org.ray.core.impl.RayNativeRuntime` → `org.ray.runtime.RayNativeRuntime`

## Cleanup
- Remove unused utility classes: CommonUtil, MD5Digestor
- Remove unused interfaces: FileStoreLink
- Remove unused exceptions: PlasmaObjectExistsException, PlasmaOutOfMemoryException
- Clean up and reformat pom.xml files
- Remove unnecessary library dependencies

## Native Code Updates
- Update JNI bindings: `org_ray_spi_impl_DefaultLocalSchedulerClient.*` → `org_ray_runtime_raylet_RayletClientImpl.*`

# Why
---
- **Simplify module structure** - Multiple modules created unnecessary complexity and implicit dependencies via reflection
- **Improve code organization** - Meaningful package names make codebase more navigable and maintainable
- **Explicit dependencies** - Eliminate reflection-based loading between modules
- **Reduce technical debt** - Remove unused/dead code and clean up dependencies