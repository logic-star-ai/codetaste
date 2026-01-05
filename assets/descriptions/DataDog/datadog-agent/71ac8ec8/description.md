# Title
-----
Remove global tagger accessor and pass tagger component via dependency injection

# Summary
-------
Refactor the tagger component to eliminate global state by removing `tagger.SetGlobalTaggerClient()` and related global accessor functions. Instead, pass the tagger component explicitly through dependency injection across all checks, listeners, and providers.

# Why
---
- **Reduce global state**: Eliminates use of global variables across the codebase, improving testability and component isolation
- **Enable component migration**: Allows migration to the latest component framework file structure
- **Better decoupling**: Remote tagger implementations (OTel, trace-agent, etc.) no longer need to import all tagger dependencies
- **Cleaner architecture**: Explicit dependency passing makes component relationships clearer

# Changes
---------

### Core Tagger Component
- Remove `global.go` containing `SetGlobalTaggerClient()`, `Tag()`, `GetEntityHash()`, etc.
- Add `LegacyTag(entity string, cardinality)` method to tagger interface for Python integration backward compatibility
- Update all tagger implementations (local, remote, replay, fake) to include `LegacyTag` method

### Component Initialization
- Add `InitSharedContainerProvider(wmeta, tagger)` called during Fx start process
- Add `GetSharedContainerProvider()` that returns error if not initialized
- Update container provider construction to accept tagger component

### Check Factories
Update all check factory signatures from `Factory(store)` to `Factory(store, tagger)`:
- Docker, Containerd, CRI, Kubelet
- Container, Generic (containers)
- Pod, ECS orchestrator checks
- OOM Kill, TCP Queue Length
- SBOM, Service Discovery

### Autodiscovery Listeners
- Create `ServiceListernerDeps` struct to bundle listener dependencies (config, telemetry, tagger, wmeta)
- Update all listener factory signatures: `NewXListener(ServiceListernerDeps)`
- Pass tagger to listeners: container, kubelet, kube_endpoints, kube_services, etc.

### Service Objects
- Add `tagger` field to service implementations
- Update `GetTags()` methods to use instance tagger instead of global

### Python Integration
- Update `initializeCheckContext()` to accept tagger parameter
- Store tagger in check context for Python checks to access
- Update `Tags()` C function to use context tagger via `LegacyTag()`

### Scheduler & Loaders
- Update `InitCheckScheduler(...)` signature to include tagger
- Update `LoaderFactory` signature: `func(SenderManager, LogReceiver, Tagger)`
- Update `LoaderCatalog()` to pass tagger to all loader factories

### Process Checks
- Pass tagger to container provider initialization
- Update resolver to use explicit container provider

### Tests
- Remove `ResetTagger()` calls (no longer needed without global)
- Update test setup to create and pass tagger instances explicitly
- Use `nooptagger` where tagger not actually needed

### Providers & Extensions
- Add tagger field to processor extensions (docker network, CRI custom metrics, etc.)
- Update `PostProcess()` signature to accept tagger parameter
- Pass tagger through processor chains

# Notes
-------
- Temporary workaround: Container provider initialization uses `fx.Invoke` during start to avoid circular dependency with workloadmeta
- Future work: Remove workloadmeta dependency from tagger to enable cleaner component structure
- All existing functionality preserved; changes are purely architectural