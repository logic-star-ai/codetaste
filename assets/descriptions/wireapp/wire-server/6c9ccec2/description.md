Title
-----
Reduce lens usage and simplify Opt/Env code

Summary
-------
Refactor options and environment handling to use native Haskell record syntax instead of lens operators, reducing complexity and improving readability.

Why
---
- Lens library adds unnecessary complexity for simple field access
- Template Haskell `makeLenses` increases compilation time
- Native record field access (`.`) is more idiomatic and readable
- Simpler code is easier to maintain

Changes
-------
**Record field access:**
- Replace lens operators (`^.`, `view`) with native `.` syntax
- Remove underscore prefixes from field names (`_host` → `host`, `_port` → `port`)
- Remove `makeLenses` calls where appropriate

**Function naming:**
- Drop `set` prefix from getter functions (`setDefaultUserLocale` → `defaultUserLocale`)
- Move default values inside functions instead of top-level constants
- Consolidate related defaults with their accessor functions

**Options structure:**
- Rename `optSettings` → `settings` for consistency
- Rename `stomp` → `stompOptions` to avoid field name conflicts
- Update JSON parsing to use `defaultOptions` instead of custom field name transformers

**Scope:**
- `libs/cassandra-util`: Options types
- `libs/wire-subsystems`: RPC implementation
- `services/brig`, `galley`, `gundeck`, `cargohold`, `spar`, `federator`: App initialization and configuration
- Test suites: Update to new field access patterns