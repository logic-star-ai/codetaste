# Refactor to eliminate global state (Viper, i18n, etc.)

## Summary
Remove all global state from Hugo by eliminating global Viper configuration access and global i18n translator. Replace with explicit dependency injection pattern passing configuration and translation providers through the dependency graph.

## Why
- Global state prevents parallel test execution (`t.Parallel`)
- Makes code harder to reason about and test
- Creates implicit dependencies and coupling
- Blocks multiple concurrent site builds with different configurations

## Changes

### Configuration
- Replace global `viper` calls with `config.Provider` interface
- Pass `*viper.Viper` instances explicitly through `deps.DepsCfg`
- Move `LoadGlobalConfig()` → `LoadConfig()` returning config instance
- Remove `viper.Reset()` from tests, create isolated instances instead

### i18n Translation
- Extract translation handling from `tpl` → new `i18n` package
- Remove global `translator` and `currentLanguage` variables
- Create `Translator` type with `Func(lang string)` method
- Add `TranslationProvider` implementing `ResourceProvider` interface
- Store translate func in `deps.Deps.Translate`

### Dependencies
- Expand `deps.DepsCfg` with explicit dependencies:
  - `Cfg config.Provider`
  - `TranslationProvider ResourceProvider`
  - `Language *helpers.Language`
- Generalize `TemplateProvider` → `ResourceProvider` pattern
- Add `LoadResources()` method loading both templates and translations

### Site & PathSpec
- Store configuration in `Site.Cfg` and `Language.Cfg`
- Move path configuration into `PathSpec` (baseURL, theme, directories, ...)
- Remove `helpers.Config()` global accessor
- Pass `config.Provider` to helper functions (e.g., `Highlight()`, `markdownify()`)

### Commands
- Introduce `commandeer` struct wrapping `DepsCfg`
- Add lazy `PathSpec()` initialization
- Store configuration state in commandeer vs. global viper

### Testing
- Enable `t.Parallel()` in test functions
- Create test helpers: `newTestCfg()`, `newTestSite()`, `newTestSourceSpec()`
- Replace `testCommonResetState()` with isolated config/fs creation
- Pass config explicitly to `buildSingleSite()` and similar functions

## Impact
- ✅ Parallel test execution now possible
- ✅ Multiple concurrent Hugo site builds supported
- ✅ Clearer dependency graph
- ✅ Easier testing and reasoning about code