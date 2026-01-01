# Remove `tracing` re-export from `bevy_utils`

## Summary

Remove the `tracing` re-export from `bevy_utils` and provide it through `bevy_log` for end-users instead. Add `tracing` as a direct dependency to internal crates that require it.

## Why

- Decouples internal crates from `bevy_utils`
- Makes eventual removal of `bevy_utils` more feasible
- Better aligns logging functionality with `bevy_log`

## Changes

**bevy_utils:**
- Mark `bevy_utils::tracing` as `doc(hidden)`
- Remove `trace_once!`, `debug_once!`, `info_once!`, `warn_once!`, `error_once!` macros
- Remove `tracing` feature and related dependencies

**bevy_log:**
- Re-export `tracing` crate for end-users
- Add `tracing` dependency
- Move `*_once!` macros from `bevy_utils` to `bevy_log`
- Update prelude to export `*_once!` macros

**Internal crates:**
- Add `tracing` as direct dependency to: `bevy_animation`, `bevy_asset`, `bevy_audio`, `bevy_core_pipeline`, `bevy_dev_tools`, `bevy_diagnostic`, `bevy_ecs`, `bevy_gilrs`, `bevy_gizmos`, `bevy_gltf`, `bevy_image`, `bevy_input_focus`, `bevy_mesh`, `bevy_pbr`, `bevy_picking`, `bevy_render`, `bevy_sprite`, `bevy_text`, `bevy_time`, `bevy_ui`, `bevy_winit`
- Update imports: `bevy_utils::tracing::*` → `tracing::*`
- Update `*_once!` macro usage: `bevy_utils::*_once!` → `bevy_log::*_once!` or import from `bevy_log`

**Examples:**
- Update imports to use `bevy::log::tracing` instead of `bevy::utils::tracing`

## Migration

Users importing `tracing` via `bevy::utils::tracing` should use `bevy::log::tracing` instead. Many common items (`warn!`, `trace!`, ...) are re-exported directly from `bevy::log`.