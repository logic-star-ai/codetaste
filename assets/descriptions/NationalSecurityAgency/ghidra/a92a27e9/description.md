Title
-----
Refactor GUI theme management to use ThemeManager pattern

Summary
-------
Refactor the `Gui` class from a monolithic static utility to a proper ThemeManager-based architecture. Move all theme management logic from static `Gui` methods into instance methods of `ThemeManager`, `ApplicationThemeManager`, and `StubThemeManager` classes.

Why
---
- Current static `Gui` class makes testing difficult and violates OOP principles
- Theme management state is scattered across static fields
- Hard to mock or substitute theme management in tests
- Poor separation of concerns between theme access and theme management

Changes
-------

**Core Architecture:**
- Create abstract `ThemeManager` base class with all theme management operations
- Create `ApplicationThemeManager` extending ThemeManager for full application use
- Create `StubThemeManager` for lightweight testing without full initialization
- Refactor `Gui` class to delegate to `ThemeManager.getInstance()` instead of containing logic
- Add `ApplicationThemeManager.initialize()` as proper initialization entry point

**Method Migration:**
- Move `setTheme()`, `addTheme()`, `deleteTheme()` from Gui → ThemeManager
- Move `getAllThemes()`, `getSupportedThemes()`, `getActiveTheme()` from Gui → ThemeManager  
- Move `setColor()`, `setFont()`, `setIcon()` from Gui → ThemeManager
- Move `restoreColor()`, `restoreFont()`, `restoreIcon()` from Gui → ThemeManager
- Move `getJavaDefaults()`, `getApplicationDarkDefaults()`, etc. from Gui → ThemeManager
- Move `hasThemeChanges()`, `isChanged*()` methods from Gui → ThemeManager
- Move LookAndFeel-related methods to ThemeManager

**Dependency Injection:**
- Update all LookAndFeelManager subclasses to accept ThemeManager in constructor
- Update ThemeDialog, ThemeUtils, ExportThemeDialog to accept ThemeManager parameter
- Update theme table models to use injected ThemeManager instead of Gui static calls
- Update theme value editors to use ThemeManager

**Refresh Logic:**
- Update `GColor.refresh()` and `GIcon.refresh()` to accept GThemeValueMap parameter
- Update `GColor.refreshAll()` and `GIcon.refreshAll()` to accept currentValues map
- Add `ThemeManager.refreshGThemeValues()` helper method

**Cleanup:**
- Rename `ThemePreferenceManager` → `ThemePreferences`
- Move `StatusReportingTaskMonitor` from GhidraRun.java to GhidraApplicationConfiguration
- Remove `getColor(id, validate)`, `getFont(id, validate)`, `getIcon(id, validate)` overloads
- Consolidate theme initialization logic into ApplicationThemeManager
- Remove static theme-related state from Gui class

**Testing:**
- Update tests to use DummyApplicationThemeManager instead of mocking static Gui
- Rename GuiTest → ThemeManagerTest
- Add proper ThemeManager instance to test setup

**Theme Properties:**
- Add `color.bg.tree`, `color.bg.tree.selected` theme properties
- Add `color.bg.plugin.programtree` theme property  
- Fix icon overlay positions for filesystem browser
- Update icon certification manifest

**Minor Fixes:**
- Fix AutoOptions editor registration order
- Update MultipleActionDockingToolbarButton.updateUI() to reinstall mouse listeners
- Add sourceIconChanged() check to DerivedImageIcon
- Update LookAndFeelUtils helper methods