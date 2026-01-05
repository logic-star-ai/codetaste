# Title
Refactor: Remove preferences and global state dependencies from tests

# Summary
Tests should not depend on `JabRefPreferences.getInstance()` or `Globals.prefs`. This refactoring introduces architectural constraints to prevent tests from accessing or modifying user preferences, ensuring test isolation and preventing accidental preference changes.

# Why
- Tests were accessing global preferences state, causing potential side effects
- Tests could accidentally change or reset user preferences
- Poor test isolation and unpredictable test behavior
- Violates good testing practices (tests should be independent and not affect system state)

# Changes

## Core Refactoring
- **KeyBindingPreferences → KeyBindingRepository**: Moved from preferences-dependent class to standalone repository
  - Logic previously in `KeyBindingPreferences` migrated to `KeyBindingRepository`
  - `Globals.getKeyPrefs()` now returns `KeyBindingRepository` instead of `KeyBindingPreferences`
  - Key binding operations (get, check equality, save) now independent of JabRefPreferences

- **PreferencesService Interface**: Created abstraction layer
  - Methods: `getJournalAbbreviationPreferences()`, `storeKeyBindingRepository()`, `getKeyBindingRepository()`, `storeJournalAbbreviationPreferences()`
  - `JabRefPreferences` implements `PreferencesService`
  - Allows mocking in tests without full preferences implementation

- **ManageJournalAbbreviations**: Refactored to accept `PreferencesService` + `JournalAbbreviationLoader` via injection
  - No longer directly accesses `JabRefPreferences`
  - `JournalAbbreviationPreferences` now has setters for mutation
  - External journal lists management decoupled from global state

## Test Changes
- Replace all `JabRefPreferences.getInstance()` → `mock(...)`
- Replace all `Globals.prefs` → injected mocks
- Mock preferences classes: `ImportFormatPreferences`, `LayoutFormatterPreferences`, `XMPPreferences`, etc.
- Use `Answers.RETURNS_DEEP_STUBS` for complex mock hierarchies

## Architecture Tests
- New test class: `TestArchitectureTests`
- Enforces: Tests must not import `JabRefPreferences` or `Globals` (except whitelisted exceptions)
- Prevents future violations through automated checks

## Affected Areas
- Importers/Exporters: BibtexImporter, EndnoteImporter, ModsExporter, ...
- Fetchers: DoiFetcher, IsbnFetcher, TitleFetcher, ...
- Layout/Formatting: LayoutTest, LatexFieldFormatterTests, ...
- Integrity checks, file operations, journal abbreviations, ...
- ~50+ test files modified