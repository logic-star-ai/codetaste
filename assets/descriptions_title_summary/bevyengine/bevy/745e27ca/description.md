# Remove `bevy_image` re-export from `bevy_render`

`bevy_render` currently re-exports everything from `bevy_image` via `pub use`, allowing code to access image types through `bevy_render::texture::*`. This re-export should be removed to improve dependency clarity and prevent accidental usage of `bevy_render` when only `bevy_image` is needed.