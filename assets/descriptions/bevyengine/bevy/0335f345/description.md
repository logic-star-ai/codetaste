# Migrate `Handle::weak_from_u128` to `weak_handle!` macro

## Summary
Replace all uses of `Handle::weak_from_u128` with the new `weak_handle!` macro introduced in #17384. Deprecate `Handle::weak_from_u128` as it's no longer needed.

## Why
- `weak_handle!` macro provides better ergonomics with UUID strings instead of u128 integers
- Makes handle creation more readable and maintainable
- Standardizes weak handle creation across the codebase
- No remaining use cases that can't be addressed by the new macro or manual construction

## Changes
- Migrate all internal shader/asset handles from `Handle::weak_from_u128(...)` to `weak_handle!("uuid-string")`
- Add `#[deprecated]` attribute to `Handle::weak_from_u128`
- Update imports to include `weak_handle` macro where needed

## Affected Areas
- `bevy_asset` ... handle deprecation
- `bevy_core_pipeline` ... auto_exposure, blit, bloom, CAS, deferred, dof, mip_generation, fullscreen, fxaa, motion_blur, OIT, post_process, skybox, SMAA, TAA, tonemapping
- `bevy_gizmos` ... line shaders
- `bevy_pbr` ... atmosphere, decals, deferred, lighting, meshlet, prepass, fog, GPU preprocess, mesh, SSAO, SSR, volumetric fog, wireframe
- `bevy_render` ... occlusion culling, globals, instance index, maths, color ops, view types, screenshot
- `bevy_sprite` ... sprite, mesh2d, color material, wireframe2d
- `bevy_ui` ... box shadow, UI shader, material pipeline, texture slice
- Examples ... mesh2d_manual