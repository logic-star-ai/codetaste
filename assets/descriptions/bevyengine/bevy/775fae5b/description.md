# Title
---
Standardize system set naming to `*Systems` convention

# Summary
---
Rename all system set types across the codebase to follow a consistent `*Systems` suffix pattern.

# Why
---
- Bevy's system set naming is wildly inconsistent: `FooSystem`, `FooSet`, `FooSystems`, or just `Foo`
- Ecosystem crates also lack consistency, making it hard for users to:
  - Choose appropriate names for their own types
  - Search for system sets on docs.rs
  - Identify which types *are* system sets
- `*Systems` is more descriptive than `*Set` - clearly indicates it's a collection of systems
- Lower risk of naming conflicts vs `*Set`
- Parallels nicely with `*Plugins` for plugin groups

# Scope
---
Rename ~30 system set types:
- `AccessibilitySystem` → `AccessibilitySystems`
- `GizmoRenderSystem` → `GizmoRenderSystems`
- `PickSet` → `PickingSystems`
- `RunFixedMainLoopSystem` → `RunFixedMainLoopSystems`
- `TransformSystem` → `TransformSystems`
- `RemoteSet` → `RemoteSystems`
- `RenderSet` → `RenderSystems`
- `SpriteSystem` → `SpriteSystems`
- `StateTransitionSteps` → `StateTransitionSystems`
- `RenderUiSystem` → `RenderUiSystems`
- `UiSystem` → `UiSystems`
- `Animation` → `AnimationSystems`
- `AssetEvents` → `AssetEventSystems`
- `TrackAssets` → `AssetTrackingSystems`
- `UpdateGizmoMeshes` → `GizmoMeshSystems`
- `InputSystem` → `InputSystems`
- `InputFocusSet` → `InputFocusSystems`
- `ExtractMaterialsSet` → `MaterialExtractionSystems`
- `ExtractMeshesSet` → `MeshExtractionSystems`
- `RumbleSystem` → `RumbleSystems`
- `CameraUpdateSystem` → `CameraUpdateSystems`
- `ExtractAssetsSet` → `AssetExtractionSystems`
- `Update2dText` → `Text2dUpdateSystems`
- `TimeSystem` → `TimeSystems`
- `EventUpdates` → `EventUpdateSystems`
- ... (several more)

# Implementation
---
- Rename types + add deprecated aliases for migration
- Update all internal usages across crates
- Update documentation referencing old names
- Add migration guide
- Add release notes encouraging ecosystem adoption

# Out of Scope
---
Types with special semantics (e.g., `Interned<dyn SystemSet>`, `EnterSchedules<S>`, `ExitSchedules<S>`, `TransitionSchedules<S>`) remain unchanged.