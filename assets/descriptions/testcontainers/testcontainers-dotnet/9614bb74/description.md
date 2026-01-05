# Title

Replace module extension methods with module API

# Summary

Refactor Testcontainers for .NET to support independent, self-contained modules by replacing extension method-based builders with dedicated builder classes and immutable configuration patterns.

# Why

The old extension method approach created tight coupling between modules and the core library. This refactoring:
- Enables modules to be maintained independently (community, OSS projects, vendors)
- Supports complex module implementations (nested configs, mixed resources, networks, volumes)
- Removes circular dependencies between modules and core library
- Provides better isolation and modularity

# Key Changes

**Builder Replacements:**
- `TestcontainersBuilder` → `ContainerBuilder`
- `TestcontainersNetworkBuilder` → `NetworkBuilder`
- `TestcontainersVolumeBuilder` → `VolumeBuilder`

**Interface Consolidation:**
- `ITestcontainersContainer` / `IDockerContainer` / `IRunningDockerContainer` → `IContainer`
- `IDockerImage` → `IImage`
- `IDockerNetwork` → `INetwork`
- `IDockerVolume` → `IVolume`

**Architectural Improvements:**
- Immutable builder state: each configuration call returns new instance
- Inheritance-based design: shared behavior across container/network/volume resources
- Default values and input validation at each level
- `ImageFromDockerfileBuilder.Build()` returns `IFutureDockerImage` (call `CreateAsync()` to build)

# Breaking Changes

Most changes are backwards compatible via obsolete attributes. Immediate migration required for:
- Classes/interfaces in the table above
- Use `ContainerBuilder` instead of `TestcontainersBuilder<TestcontainersContainer>`
- `ImageFromDockerfileBuilder.Build()` → `.Build().CreateAsync()`

All obsolete classes/interfaces moved to `_OBSOLETE_/` and `BackwardCompatibility/` namespaces.

# Implementation Details

- New `AbstractBuilder<TBuilderEntity, TResourceEntity, TConfigurationEntity>` base class
- Added `Resource` base class with common `Exists()` / `ThrowIfResourceNotFound()` logic
- Configuration classes renamed: `ITestcontainersConfiguration` → `IContainerConfiguration`, etc.
- New `IFutureResource` interface for resources requiring explicit creation
- Parameter naming improvements (`privatePort` → `containerPort`, `oldValue` / `newValue` convention)