# Remove global `events.Default` singleton and pass `events.Logger` explicitly

Eliminate the global `events.Default` singleton by converting `events.Logger` to an interface and passing instances explicitly throughout the codebase. Add `events.NoopLogger` for contexts where event logging is not needed.