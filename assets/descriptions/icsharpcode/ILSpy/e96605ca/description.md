# Title

Replace singletons with DI patterns and decouple service dependencies

# Summary

Refactor UI layer architecture to replace singleton pattern with dependency injection, eliminating direct static dependencies between services.

# Why

- Current singleton pattern (`SettingsService.Instance`, `LanguageService.Instance`, `DockWorkspace.Instance`, etc.) creates tight coupling
- Difficult to test components in isolation
- Hard to manage service lifetimes and dependencies
- Poor separation of concerns

# What Changed

**Removed Singleton Instances:**
- `SettingsService.Instance` → Constructor-injected
- `LanguageService.Instance` → Constructor-injected  
- `DockWorkspace.Instance` → Constructor-injected
- `MainWindow.Instance` → MEF-exported singleton

**Dependency Injection:**
- Added `[Export]`/`[Shared]` MEF attributes throughout
- Constructor injection for services (commands, view models, language implementations, ...)
- `IExportProvider` used for dynamic resolution
- Services registered in `App.xaml.cs` DI container

**Communication Patterns:**
- Introduced `MessageBus<T>` for decoupled event communication
- Events for navigation, settings changes, layout updates, ...
- Static protected properties in base classes (`Language`, `SettingsService`, `AssemblyTreeModel`, ...) for common services

**Updated Components:**
- Commands receive dependencies via constructor
- Tree nodes use protected static properties for services
- Analyzers use injected `AssemblyList`
- View models properly injected with required services
- Language implementations receive dependencies

**New Infrastructure:**
- `GlobalUtils` for process/link operations (extracted from `MainWindow`)
- `UpdateService` replaces `NotifyOfUpdatesStrategy`
- `UpdatePanelViewModel` + view for update notifications
- Parameter binding support via `IProvideParameterBinding`

# Notes

- **No functional changes** - purely architectural refactoring
- Maintains backward compatibility where possible
- Some base classes still use static accessors for common services (pragmatic trade-off)
- Message bus enables loose coupling between components