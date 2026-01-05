Title
-----
Remove global `events.Default` singleton and pass `events.Logger` explicitly

Summary
-------
Eliminate the global `events.Default` singleton by converting `events.Logger` to an interface and passing instances explicitly throughout the codebase. Add `events.NoopLogger` for contexts where event logging is not needed.

Why
---
- Removes global state, improving testability and modularity
- Makes event logging dependencies explicit
- Allows different components to have isolated event streams if needed

Changes
-------

**Events package:**
- Convert `events.Logger` to interface, rename concrete type to `logger`
- Add `events.NoopLogger` implementation for test/non-logging contexts
- Add `Subscription.Unsubscribe()` method (was `Logger.Unsubscribe(sub)`)
- Remove global `events.Default` singleton

**Config wrapper:**
- Add `evLogger events.Logger` parameter to `config.Load()` and `config.Wrap()`
- Config wrapper no longer emits `events.ConfigSaved` directly
- Calling code responsible for logging config-related events

**Throughout codebase:**
- Pass `events.Logger` to constructors/functions: `model.NewModel()`, `api.New()`, `connections.NewService()`, `discover.NewGlobal()`, `discover.NewLocal()`, `NewFolderSummaryService()`, `newFolder()`, `NewProgressEmitter()`, etc.
- Update all event subscriptions: `evLogger.Subscribe(...)` and `sub.Unsubscribe()`
- Replace `events.Default.Log(...)` with `evLogger.Log(...)`

**cmd/syncthing:**
- Create `events.Logger` instance in `syncthingMain()`
- Pass to all subsystems
- Auto-upgrade: Subscribe to events via passed logger instead of global

**Tests:**
- Use `events.NoopLogger` in unit tests where events not needed
- Create/serve/stop `events.Logger` in tests that verify event behavior