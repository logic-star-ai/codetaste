# Remove print statements and replace with proper logging

## Summary
Remove all `print()` statements from production code (excluding UI tests) and replace critical ones with proper `Logger` usage. Clean up dead debugging code discovered during the process.

## Why
- Print statements clutter console output and provide no structured logging
- No ability to control log levels or categorize output
- Print statements in production code are not best practice
- Should use `Logger` infrastructure for proper observability

## Changes

### Print Statement Removal
- Remove print statements from Account, Client, Storage, Providers, RustFxA, WidgetKit, and content-blocker-lib-ios modules
- Preserve print statements in UI tests for automation team debugging purposes

### Replace with Proper Logging
- FxATelemetry: telemetry decode errors → `logger.log(..., level: .warning, category: .telemetry)`
- AppLaunchUtil: RustFirefoxAccounts startup → `logger.log(..., level: .info, category: .sync)`
- Authenticator: missing hostname warnings → `logger.log(..., level: .warning, category: .sync)`
- BrowserViewController: WebContent process crashes → `logger.log(..., level: .warning, category: .webview)`
- DownloadsPanel: file deletion errors → `logger.log(..., level: .warning, category: .library)`
- SyncStatusResolver: sync status updates → `logger.log(..., level: .info, category: .sync)`
- FxAWebViewModel: origin mismatch warnings → `logger.log(..., level: .warning, category: .sync)`

### Add Logger Support
- Add `LoggerCategory.telemetry` enum case
- Add `logger: Logger` parameters to relevant initializers/functions:
  - `FxATelemetry.parseTelemetry(...)`
  - `Authenticator.showAuthenticationDialog(...)`
  - `DownloadsPanel.init(...)`
  - `SyncStatusResolver.init(...)`
  - `FxAWebViewModel.init(...)`

### Dead Code Removal
- Remove `PerformanceTimer` class from Shared/GeneralUtils.swift (unused profiling utility)
- Remove SQLite debugging infrastructure from Storage/ThirdParty/SwiftData.swift:
  - `debug_enabled` flag
  - `traceOn()` function
  - `explain(query:withArgs:)` function
  - All conditional debug logging blocks
- Remove duplicate error logging in BrowserSchema.swift
- Remove unused Common import from main.swift
- Convert empty catch blocks with prints to empty catch blocks
- Remove print statements from assertion-only code paths

### Scope
Files affected: ~40 files across Account, Client, Storage, Providers, RustFxA, Shared, WidgetKit, content-blocker-lib-ios, and Tests modules