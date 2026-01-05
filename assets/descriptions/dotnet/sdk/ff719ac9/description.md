# Refactor Hot Reload client for code sharing with VS/VS Code

## Summary
Refactor Hot Reload delta applier code to prepare for sharing with Visual Studio and VS Code by:
- Replacing `IReporter` with `ILogger` abstraction
- Creating `Microsoft.DotNet.HotReload.Client` source package
- Removing Roslyn dependencies from shared code
- Renaming `DeltaApplier` → `HotReloadClient` 
- Improving testability and abstractions

## Changes

### Logging & Abstractions
- Replace `IReporter` with `ILogger` (`Microsoft.Extensions.Logging`) for message reporting
- Restrict `IReporter` usage to abstracting `ConsoleReporter` for testing only
- Add `IProcessOutputReporter` for process output handling
- Introduce `IHotReloadAgent` abstraction for testing

### Code Organization
- Create `Microsoft.DotNet.HotReload.Client` source package (`.shproj` + `.csproj`)
- Move shareable code to package (targets `netstandard2.0` + `$(SdkTargetFramework)`)
- Extract `PipeListener` class from `StartupHook` for testability
- Add `.editorconfig` configurations for source package consumers

### Naming & Types
- Rename `DeltaApplier` → `HotReloadClient`
- Rename `UpdateDelta` → `RuntimeManagedCodeUpdate`
- Rename `StaticAssetUpdate` → `RuntimeStaticAssetUpdate`  
- Rename `ApplyDeltas()` → `ApplyManagedCodeUpdates()`
- Replace `BlazorWebAssemblyHostedDeltaApplier` with general `HotReloadClients` (plural) for broadcasting

### Suspended Process Support
- Handle pending responses before next request when debugger is attached
- Track pending updates via `_pendingUpdates` task chain
- Send/receive updates asynchronously without blocking when process suspended

### Testing
- Add `HotReloadClientTests` with scenarios for suspended/non-suspended processes
- Add `TestHotReloadAgent` mock
- Improve test utilities (`TestLogger`, `TestProcessOutputReporter`)
- Remove obsolete `StartupHookTests.IsMatchingProcess` tests

### Environment & Configuration
- Remove `DOTNET_WATCH_HOTRELOAD_TARGET_PROCESS_PATH` environment variable (obsolete)
- Make `ProcessCleanupTimeout` nullable (configurable per mode)
- Add `SuppressBrowserRefresh` to `EnvironmentVariables.Names`
- Fix typo: `DiagnosticsSource` → `DiagnosticSource` (package version property)

### Message Descriptors
- Convert to static `MessageDescriptor` pattern with structured logging
- Add `LogEvents` class with `EventId` tracking
- Consolidate message formatting logic
- Add component-specific logger names (`BrowserConnection:Server`, `BrowserConnection:Agent`, etc.)

## Why
Enables code sharing with Visual Studio and VS Code by:
- Using framework-standard logging abstractions
- Packaging shareable code as source package
- Removing product-specific dependencies
- Supporting debugger scenarios (suspended processes)

Fixes #42921