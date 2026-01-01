# Rename `Swift*Tool` to `Swift*Command`

## Summary
Rename all `Swift*Tool` types to `Swift*Command` and `SwiftTool` to `SwiftCommandState` to eliminate naming confusion with plugin build tools.

## Why
- `SwiftBuildTool` (CLI invocation handler) vs. build tools in plugins creates confusion when working on plugin codebase
- `SwiftTool` is actually a state container for CLI commands, not a tool itself → rename to `SwiftCommandState` for clarity

## Changes
**Core renamings:**
- `SwiftBuildTool` → `SwiftBuildCommand`
- `SwiftRunTool` → `SwiftRunCommand`
- `SwiftTestTool` → `SwiftTestCommand`
- `SwiftPackageTool` → `SwiftPackageCommand`
- `SwiftTool` → `SwiftCommandState`
- `SwiftSDKTool` → `SwiftSDKCommand`
- `PackageCollectionsTool` → `PackageCollectionsCommand`
- `PackageRegistryTool` → `PackageRegistryCommand`

**Related renamings:**
- `*ToolOptions` → `*CommandOptions`
- `CompletionTool` → `CompletionCommand`
- `ToolWorkspaceDelegate` → `CommandWorkspaceDelegate`
- `SwiftToolObservabilityHandler` → `SwiftCommandObservabilityHandler`
- `swiftTool` parameters → `swiftCommandState`
- Directory: `PackageTools/` → `PackageCommands/`
- Modules: `*Tool` → `*Command`

## Scope
- All command implementations
- Test files
- CMake/build configuration
- Package.swift manifest
- Documentation/comments