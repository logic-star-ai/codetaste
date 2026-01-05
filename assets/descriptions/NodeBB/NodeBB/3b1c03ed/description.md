# Title
Refactor: Move plugin hook methods to `plugin.hooks.*` namespace

## Summary
Reorganize plugin hook methods (`fireHook`, `registerHook`, `hasListeners`, `unregisterHook`) into dedicated `plugins.hooks.*` namespace for better code organization and separation of concerns.

## Why
- Hook-related functionality scattered across main `plugins` object
- Better module organization by grouping related methods
- Clearer API surface for hook operations
- Improves code maintainability and discoverability

## Changes Made

### Core Refactoring
- Extract hook methods from `src/plugins/index.js` to new `src/plugins/hooks.js` module
- Create `Hooks` object with methods:
  - `fire()` (formerly `fireHook()`)
  - `register()` (formerly `registerHook()`)
  - `unregister()` (formerly `unregisterHook()`)
  - `hasListeners()`
- Move hook-related internals (`deprecatedHooks`, `internals`, etc.)

### API Updates
- Replace `plugins.fireHook()` → `plugins.hooks.fire()` across codebase
- Replace `plugins.registerHook()` → `plugins.hooks.register()` 
- Replace `plugins.hasListeners()` → `plugins.hooks.hasListeners()`
- Replace `plugins.unregisterHook()` → `plugins.hooks.unregister()`

### Backwards Compatibility
- Keep aliased methods on `plugins.*` for compatibility
- Add deprecation notice (removal planned for v1.16.0)

## Scope
Updated ~200+ call sites across:
- Analytics, API helpers, authentication, controllers...
- Categories, groups, messaging, notifications...
- Posts, topics, user management, privileges...
- Admin interface, middleware, socket.io handlers...
- Widgets, rewards, search, and more

## Result
- Cleaner namespace: `plugins.hooks.fire()` vs `plugins.fireHook()`
- Dedicated module for hook operations
- Maintained backward compatibility
- Consistent API throughout codebase