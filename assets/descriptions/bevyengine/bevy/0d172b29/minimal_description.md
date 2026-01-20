# Refactor: Consolidate logging imports to use `bevy_utils::tracing`

Replace all uses of `bevy_log`'s tracing reexport with `bevy_utils::tracing` for consistent logging across the codebase.