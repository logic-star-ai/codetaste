# Remove `tracing` re-export from `bevy_utils`

Remove the `tracing` re-export from `bevy_utils` and provide it through `bevy_log` for end-users instead. Add `tracing` as a direct dependency to internal crates that require it.