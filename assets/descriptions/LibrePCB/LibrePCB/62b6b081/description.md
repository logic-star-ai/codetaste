Title
-----
Remove QtWidgets dependency from CLI and core library

Summary
-------
Refactor the `Application` class to eliminate QtWidgets dependency from the CLI binary and core library. Convert `Application` from a `QApplication` subclass to a static utility class, enabling the CLI to run with `QGuiApplication` instead.

Why
---
- Cleaner architecture with better separation of concerns
- CLI should not depend on widget-related functionality
- Potentially allows CLI to run without X-Server
- Follows separation between GUI and non-GUI code

Changes
-------
**Application Class Refactoring:**
- Convert `Application` from `QApplication` subclass to static utility class
- Change all instance methods to static methods (e.g., `getVersion()`, `getFileFormatVersion()`, `getResourcesDir()`, ...)
- Remove all member variables, replace with static initialization where needed
- Move font loading to static `loadBundledFonts()` method
- Move translation setup to static `setTranslationLocale()` method

**Binary-Specific Changes:**
- CLI: Use `QGuiApplication` instead of `Application`
- GUI: Use `QApplication` directly instead of `Application`
- Update `main()` functions in both binaries accordingly

**Core Library:**
- Remove QtWidgets dependency from `CMakeLists.txt`
- Change includes from `<QtWidgets>` to `<QtCore>` or `<QtGui>` where appropriate
- Replace all `qApp->...` calls with `Application::...` static calls
- Move Qt meta type registration to new `QtMetaTypeRegistration` helper class

**Stroke Font Pool:**
- Make `StrokeFontPool` initialization thread-safe using static const
- Add `exists()` method to check font availability

**Miscellaneous:**
- Move `detectRuntime()` from `Application` to `SystemInfo`
- Update all references throughout codebase (exporters, painters, dialogs, widgets, ...)
- Replace `qApp->quitTriggered` signal with `QApplication::closeAllWindows()` calls