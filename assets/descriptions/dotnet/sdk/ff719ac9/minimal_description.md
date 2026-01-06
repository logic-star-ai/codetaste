# Refactor Hot Reload client for code sharing with VS/VS Code

Refactor Hot Reload delta applier code to prepare for sharing with Visual Studio and VS Code by:
- Replacing `IReporter` with `ILogger` abstraction
- Creating `Microsoft.DotNet.HotReload.Client` source package
- Removing Roslyn dependencies from shared code
- Renaming `DeltaApplier` → `HotReloadClient` 
- Improving testability and abstractions