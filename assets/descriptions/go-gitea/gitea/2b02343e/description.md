# Title
Refactor `setting` package to improve testability and structure

## Summary
Split configuration initialization and loading logic to make unit testing easier. Separate settings into categorized files and improve function naming consistency.

## Changes

### Configuration Provider Abstraction
- Introduce `ConfigProvider` interface to abstract ini.File usage
- Split `LoadFromXXX()` functions into:
  - `InitProviderFromXXX()` - creates/initializes ini file provider
  - `LoadCommonSettings()` - loads actual settings from provider
- Replace direct `Cfg` global access with `ConfigProvider` parameter in load functions

### Function Naming Consistency  
- Rename `newXXXService()` → `loadXXXFrom(rootCfg ConfigProvider)` or `loadXXXSetting()`
- Rename `NewXORMLogService()` → `InitSQLLog()`
- Rename `NewLogServices()` → `InitLogs()`
- Rename `NewServices()` → `LoadSettings()`
- Rename `NewServicesForInstall()` → `LoadSettingsForInstall()`

### Setting Organization
Split monolithic settings into categorized files:
- `admin.go`, `api.go`, `camo.go`, `config_provider.go`, `cors.go`, `highlight.go`, `incoming_email.go`, `metrics.go`, `oauth2.go`, `other.go`, `security.go`, `server.go`, `ssh.go`, `time.go`, `ui.go`
- Move related settings (Admin, API, Camo, Metrics, UI, etc.) to dedicated files
- Extract helper functions (e.g., `deprecatedSetting`, `mustMapSetting`)

### Global Variable Consolidation
- Group log settings under `Log` struct (Level, RootPath, EnableXORMLog, etc.)
- Move session settings to `SessionConfig` struct with `OriginalProvider` field
- Centralize security-related settings

### Test Improvements
- Add `InitProviderAndLoadCommonSettingsForTest()` for test initialization
- Support `extraConfigs` parameter for test-specific configuration

## Why
- Current monolithic `loadFromConf()` makes unit testing difficult
- Tight coupling to global `Cfg` variable prevents isolated testing
- Inconsistent function naming (`newXXX` vs actual behavior) causes confusion
- Large setting.go file (~1500+ lines) hard to navigate and maintain
- Better separation of concerns improves code organization and testability