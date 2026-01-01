# Title
-----
Rename `Logger` to `LegacyLogger` to avoid naming conflict with BrowserKit

# Summary
-------
Rename the existing `Logger` struct to `LegacyLogger` across the entire codebase to prevent name collision when introducing the new `Logger` from BrowserKit.

# Why
---
Starting to integrate BrowserKit's `Logger`, which conflicts with our current `Logger` implementation. Need to disambiguate by marking our existing logger as "legacy" before transitioning.

# Changes
---------
- Rename `Shared/Logger.swift` → `Shared/LegacyLogger.swift`
- Rename `public struct Logger {}` → `public struct LegacyLogger {}`
- Update all references throughout codebase:
  - `Logger.syncLogger` → `LegacyLogger.syncLogger`
  - `Logger.browserLogger` → `LegacyLogger.browserLogger`
  - `Logger.keychainLogger` → `LegacyLogger.keychainLogger`
  - `Logger.corruptLogger` → `LegacyLogger.corruptLogger`
  - `Logger.copyPreviousLogsToDocuments()` → `LegacyLogger.copyPreviousLogsToDocuments()`
- Update Xcode project file references

# Files Affected
---------------
- `Shared/LegacyLogger.swift` (renamed)
- `Account/...`, `Client/...`, `Extensions/...`, `Providers/...`, `Push/...`, `Storage/...`, `Sync/...`, `SyncTelemetry/...`, `Tests/...`
- ~50+ files with logger references updated