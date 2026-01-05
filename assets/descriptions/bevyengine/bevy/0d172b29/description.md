# Refactor: Consolidate logging imports to use `bevy_utils::tracing`

## Summary
Replace all uses of `bevy_log`'s tracing reexport with `bevy_utils::tracing` for consistent logging across the codebase.

## Why
Currently, bevy crates inconsistently switch between using `bevy_utils::tracing` and `bevy_log` for accessing logging macros. This creates unnecessary confusion and dependency bloat.

Since all affected crates already depend on `bevy_utils`, using its tracing reexport provides consistency without additional overhead.

## Changes

### Import Statements
Replace:
```rust
use bevy_log::{error, warn, debug, info, trace};
```

With:
```rust
use bevy_utils::tracing::{error, warn, debug, info, trace};
```

### Cargo.toml
- Remove `bevy_log` dependency from crates where it's no longer needed after the refactor
- Keep it only where actually required (e.g., for the `LogPlugin` itself)
- Move to `dev-dependencies` where only tests/examples need it

### Affected Crates
- `bevy_animation`
- `bevy_asset`
- `bevy_core_pipeline`
- `bevy_diagnostic`
- `bevy_gilrs`
- `bevy_gizmos`
- `bevy_gltf`
- `bevy_hierarchy`
- `bevy_render`
- `bevy_sprite`
- `bevy_ui`

### Macros
All logging macros: `error!`, `warn!`, `info!`, `debug!`, `trace!`, `info_span!`, `warn_once!`