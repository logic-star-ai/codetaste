Title
-----
Eliminate `share` module and relocate classes to `server` and `server-common`

Summary
-------
Remove the `share` module and redistribute its classes to appropriate modules based on usage patterns and dependencies.

Why
---
The `share` module is unnecessary and creates additional module complexity. Classes should be placed directly in `server` or `server-common` based on their actual usage and dependency requirements.

Changes Required
----------------

**Module Reorganization:**
- Move Share Fetch, Acknowledge, Session, Context, and Cache classes → `server` module (used by `core` and `tools`)
- Move Persister classes and `SharePartitionKey` → `server-common` module (future usage by `group-coordinator`)

**Build Configuration:**
- Remove `:share` project definition from `build.gradle`
- Remove `:share` dependencies from `:core`, `:share-coordinator`, and `:tools` modules

**Import Controls:**
- Delete `checkstyle/import-control-share.xml`
- Update `checkstyle/import-control-server-common.xml` to include `share` subpackage rules

**File Relocations:**
- `share/src/.../server/share/persister/*` → `server-common/src/.../server/share/persister/*`
- `share/src/.../server/share/{fetch,session,context,acknowledge}/*` → `server/src/.../server/share/{...}/*`
- `share/src/.../server/share/CachedSharePartition.java` → `server/src/.../server/share/`
- Move all corresponding test files to match new structure

Rationale
---------
**Persister → server-common**: Abstraction for share group progress persistence; will be consumed by `group-coordinator` module in near future, making it more server-related than coordinator-specific.

**Fetch/Session/Cache → server**: Directly consumed by `core` and `tools` modules; no need for separate module layer.