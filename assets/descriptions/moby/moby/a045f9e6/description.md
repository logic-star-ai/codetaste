# Title
-----
Migrate container, image, and storage types to dedicated packages

# Summary
-------
Reorganize API types from the monolithic `api/types` package into domain-specific packages (`container`, `image`, `storage`) to improve code organization and reduce coupling.

# Why
---
- Single `api/types` package contains mixed domain types (containers, images, networks, storage)
- Better separation of concerns needed
- Avoid circular dependencies (e.g., `GraphDriverData` shared between images and containers)
- Improve API structure and maintainability

# Changes
---------

**Container types** → `api/types/container`:
- `NetworkSettings`, `NetworkSettingsBase`, `DefaultNetworkSettings`
- `SummaryNetworkSettings` → `NetworkSettingsSummary`
- `Health`, `HealthcheckResult` + health status constants
- `MountPoint`, `Port`
- `ContainerState` → `State`
- `Container` → `Summary`
- `ContainerJSONBase` → `InspectBase`
- `ContainerJSON` → `InspectResponse`
- `ContainerNode` (deprecated, will be removed)

**Image types** → `api/types/image`:
- `ImageInspect` → `InspectResponse`
- `RootFS`

**Storage types** → `api/types/storage` (new package):
- `GraphDriverData` → `DriverData`

# Implementation
--------------
- Move type definitions to new locations
- Create deprecation aliases in `api/types/types_deprecated.go`
- Update all references across daemon, client, CLI, integration tests
- Update Swagger spec
- Update generator scripts