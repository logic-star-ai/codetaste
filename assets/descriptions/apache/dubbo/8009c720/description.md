# Title
-----
Refactor application lifecycle management with SPI-based `ApplicationLifecycle` interface

# Summary
-------
Introduce `ApplicationLifecycle` SPI to distribute lifecycle management across modules, replacing centralized logic in `DefaultApplicationDeployer` with modular, ordered implementations.

# Why
---
- **Decouple `dubbo-config-api`**: Invert dependencies so external modules depend on config-api, not vice versa
- **Modularize lifecycle logic**: Each module manages its own lifecycle instead of centralized in `DefaultApplicationDeployer`
- **Simplify deployer**: Reduce `DefaultApplicationDeployer` to pure process management without lifecycle state fields

# What
----
### Core Changes
- Add `ApplicationLifecycle` SPI with methods:
  - `initialize()`, `start()`, `preDestroy()`, `postDestroy()`
  - `preModuleChanged()`, `postModuleChanged()`, `refreshServiceInstance()`
- Add `ApplicationLifecycleManager` to orchestrate implementations via `@Activate` ordering
- Add `ApplicationContext` to aggregate lifecycle-related state
- Extract lifecycle logic from `DefaultApplicationDeployer` into implementations:
  - `ApplicationConfigPreHandleLifecycle` / `ApplicationConfigPostHandleLifecycle` - config loading
  - `ConfigCenterApplicationLifecycle` - config center initialization
  - `MetadataInitializeLifecycle` / `MetadataApplicationLifecycle` / `MetadataDestroyApplicationLifecycle` - metadata management
  - `MetricsInitializeLifecycle` / `MetricsExportApplicationLifecycle` / `MetricsCollectorStartLifecycle` - metrics handling
  - `ObservationRegistryApplicationLifecycle` - tracing initialization
  - `RegisterApplicationLifecycle` / `DeregisterApplicationLifecycle` - service registration/deregistration
  - `ApplicationPreOfflineLifecycle` / `ModuleOfflineLifecycle` - service offline operations
  - ... (and more)

### Implementation Details
- Lifecycle implementations ordered via `@Activate(order = ...)` to ensure correct execution sequence
- `AbstractDeployer` state fields changed to `AtomicReference`/`AtomicBoolean` for thread safety
- Create new `dubbo-configcenter-api` module to hold config center lifecycle
- Each module declares its lifecycle implementations in `META-INF/dubbo/internal/...ApplicationLifecycle` SPI files
- Lifecycle implementations temporarily kept in `dubbo-config-api` until dependency decoupling completes

### Call Sequence
```
initialize: 
  ApplicationConfigPreHandleLifecycle -> ConfigCenterApplicationLifecycle -> 
  ApplicationConfigPostHandleLifecycle -> MetadataInitializeLifecycle -> 
  MetricsInitializeLifecycle -> ObservationRegistryApplicationLifecycle -> 
  ModuleInitializeLifecycle

preDestroy:
  ApplicationPreOfflineLifecycle -> MetricsDisableApplicationLifecycle -> 
  ApplicationPostOfflineLifecycle

postDestroy:
  DeregisterApplicationLifecycle -> MetadataDestroyApplicationLifecycle
```

# Changes
---------
- `org.apache.dubbo.config.deploy.lifecycle.Lifecycle` - base lifecycle interface
- `org.apache.dubbo.config.deploy.lifecycle.application.ApplicationLifecycle` - application-level lifecycle SPI
- `org.apache.dubbo.config.deploy.lifecycle.manager.ApplicationLifecycleManager` - orchestrates all implementations
- `org.apache.dubbo.config.deploy.context.ApplicationContext` - holds lifecycle state
- `org.apache.dubbo.common.deploy.AbstractDeployer` - thread-safe state fields
- `org.apache.dubbo.config.deploy.DefaultApplicationDeployer` - simplified to delegate to lifecycle manager
- New module: `dubbo-configcenter-api`