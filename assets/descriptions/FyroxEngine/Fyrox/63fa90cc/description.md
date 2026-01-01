Title
-----
Refactor resource system - consolidate metadata in ResourceHeader

Summary
-------
Refactor internal structure of resources to centralize all metadata (path, type UUID, state) in a single `ResourceHeader` struct instead of scattering across `ResourceState` variants and resource data implementations.

Why
---
Current architecture spreads resource metadata across multiple locations making it difficult to add new fields (e.g., per-resource UUID) and maintain consistency. Consolidation improves maintainability and flexibility.

Changes
-------
**Core Structure**
- Introduce `ResourceHeader { kind, type_uuid, state }` to hold all resource metadata
- Add `ResourceKind` enum (Embedded/External) to replace path-based logic
- Replace `UntypedResource(Arc<Mutex<ResourceState>>)` with `UntypedResource(Arc<Mutex<ResourceHeader>>)`

**ResourceData Trait**
- Remove `path()`, `set_path()`, `is_embedded()` methods
- Keep only `as_any()`, `as_any_mut()`, `type_uuid()`, `save()`

**Resource Loaders**
- Change `load()` signature from managing state to returning `Result<LoaderPayload, LoadError>`
- Remove `event_broadcaster` and `reload` parameters
- Loaders now just load data, not manage state

**Resource State**
- Remove path/type_uuid from `ResourceState::Pending` and `LoadError` variants
- Simplify commit methods - no longer need path parameter

**API Changes**
- `Resource::new_ok()` requires `ResourceKind` parameter
- `Resource::new_pending()` requires `ResourceKind` parameter  
- `resource.path()` → `resource.kind().path()`
- `resource.set_path()` → `resource.set_kind()`

**Updates**
- Update all resource types: Texture, Model, Shader, Material, SoundBuffer, Curve, HrirSphere
- Update all loaders to new interface
- Update editor/examples usage patterns
- Implement backward compatibility in visitor

Benefits
--------
- ✅ Centralized metadata in single location
- ✅ Cleaner separation of concerns
- ✅ Easier to add new fields (UUID, etc.) without breaking changes
- ✅ Simpler loader implementations
- ✅ Backward compatibility preserved
- ✅ More flexible resource system architecture