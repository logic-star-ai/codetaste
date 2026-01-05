Title
-----
Replace offensive terminology with inclusive language (Part 1)

Summary
-------
Refactor codebase to replace "master/slave" terminology with inclusive alternatives like "main", "leader", and "primary". This addresses terminology in control objects, audio paths, variables, methods, and UI elements.

Why
---
Remove potentially offensive language from the codebase to align with inclusive software development practices.

Changes
-------
**Control Objects & Audio Paths:**
- Rename `master` control key → `main_mix` (with backward-compatible alias)
- Replace `sync_master` → `sync_leader`
- Refactor `AudioPath` types to `AudioPathType` enum class with proper naming:
  - `MASTER` → `Main`
  - `VINYLCONTROL` → `VinylControl`
  - `MICROPHONE` → `Microphone`
  - `AUXILIARY` → `Auxiliary`
  - ...

**Internal API:**
- `getMasterBuffer()` → `getMainBuffer()`
- `isMasterEnabled()` → `isMainMixEnabled()`
- `setMaster()` → `setMainMix()`
- `m_pMaster*` variables → `m_pMain*`
- `MicMonitorMode::MASTER*` → `MicMonitorMode::Main*`
- ...

**UI & Configuration:**
- Update preferences dialog labels/controls
- Update skin XML files
- Update controller mappings
- Update schema documentation

**Tests:**
- Rename test reference buffers (`*-master` → `*-main`)
- Update test expectations

**Backward Compatibility:**
- Add control object aliases to maintain compatibility with existing configurations/mappings

Scope
-----
This refactoring covers control objects, audio engine internals, UI elements, and test infrastructure. Does not include `[Master]` CO group rename or `EngineMaster` class rename (deferred to future work).