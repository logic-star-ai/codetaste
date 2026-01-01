# Title
-----
Remove `bevy_image` re-export from `bevy_render`

# Summary
-------
`bevy_render` currently re-exports everything from `bevy_image` via `pub use`, allowing code to access image types through `bevy_render::texture::*`. This re-export should be removed to improve dependency clarity and prevent accidental usage of `bevy_render` when only `bevy_image` is needed.

# Why
---
- Users may accidentally depend on `bevy_render` when they only need image functionality
- Blurs the boundary between rendering and image handling concerns
- Makes dependency graph less clear

# Solution
--------
- Remove the `pub use` statement from `bevy_render`
- Update all internal imports from `bevy_render::texture::{Image, ...}` to `bevy_image::{Image, ...}`
- Add `bevy_image` dependency to crates that relied on the re-export:
  - `bevy_gizmos`
  - `bevy_pbr`
  - `bevy_sprite`
  - `bevy_text`
  - `bevy_ui`
- Expose `bevy_image` as `bevy::image` in the main crate
- Update `AsBindGroup` macro codegen to use correct paths
- Fix imports across examples

# Affected Items
--------------
- Image types: `Image`, `ImageFormat`, `ImageSampler`, `ImageSamplerDescriptor`, `ImageFilterMode`, `ImageAddressMode`, `ImageLoaderSettings`, `ImageType`
- Traits/extensions: `BevyDefault`, `TextureFormatPixelInfo`, `CompressedImageFormats`
- Loaders: `ImageLoader`, `ExrTextureLoader`, `HdrTextureLoader`
- `bevy_render::texture::*` → `bevy_image::*`

# Migration
----------
Replace `bevy_render::texture::*` imports with `bevy_image::*` or use the new `bevy::image::*` path.