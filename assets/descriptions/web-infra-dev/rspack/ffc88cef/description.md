# Title
-------
Refactor: Module build methods to directly update `build_info` and `build_meta`, remove `Option` wrappers

# Summary
-------
Simplify module build API by having `Module::build()` directly update internal `build_info` and `build_meta` fields instead of returning them, and remove `Option` wrappers from trait methods.

# Why
---
Current design has unnecessary indirection where `BuildResult` contains `build_info` and `build_meta`, which are then set on the module after `build()` completes. This creates unnecessary complexity and makes it unclear when these fields are populated.

# Changes
---

**1. `BuildResult` structure**
- Remove `build_meta: BuildMeta` field
- Remove `build_info: BuildInfo` field
- Only contains `dependencies`, `blocks`, `optimization_bailouts`

**2. `Module` trait methods**
```diff
- fn build_info(&self) -> Option<&BuildInfo>
+ fn build_info(&self) -> &BuildInfo

- fn build_meta(&self) -> Option<&BuildMeta>
+ fn build_meta(&self) -> &BuildMeta

- fn set_build_info(&mut self, info: BuildInfo)
+ fn build_info_mut(&mut self) -> &mut BuildInfo

- fn set_build_meta(&mut self, meta: BuildMeta)
+ fn build_meta_mut(&mut self) -> &mut BuildMeta
```

**3. Module implementations**
- Initialize `build_info` and `build_meta` with `Default::default()` instead of `None`
- Update fields directly in `build()`: `self.build_info = ...`, `self.build_meta = ...`
- Remove `Option` handling throughout codebase

**4. Callsites**
- Remove `Option` unwrapping (`if let Some(build_info) = ...` → direct access)
- Replace `set_build_info(...)` → `*module.build_info_mut() = ...`
- Replace `set_build_meta(...)` → `*module.build_meta_mut() = ...`

# Scope
---
- `NormalModule`, `ContextModule`, `ExternalModule`, `RawModule`, `SelfModule`
- `ConcatenatedModule`, `DllModule`, `DelegatedModule`
- `ContainerEntryModule`, `FallbackModule`, `RemoteModule`
- `ConsumeSharedModule`, `ProvideSharedModule`
- `LazyCompilationProxyModule`, `CssModule`
- All callsites in build/cache/stats/plugin infrastructure