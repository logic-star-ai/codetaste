# Move WindowUUID into Common module

## Summary
Move `WindowUUID` type and its extensions from the `Client` module into `BrowserKit/Sources/Common` to improve code organization and make it accessible across all modules.

## Why
- `WindowUUID` is a fundamental type used throughout the app for window identification
- Current location in `Client` limits its accessibility to other modules
- Moving to `Common` improves architecture by making it available in `BrowserKit` and reduces module coupling
- Enables consistent type usage across Redux actions, coordinators, view models, and UI components

## Changes
- Move `WindowUUID+Extension.swift` from `Client/Extensions/` to `BrowserKit/Sources/Common/`
- Update type signatures: replace `UUID` with `WindowUUID` where used for window identification in...
  - Redux `Action` classes
  - `ThemeManager` and `Themeable` protocols
  - Coordinators, view models, and state objects
  - All window-specific functionality
- Add `import Common` statements across affected files
- Remove hardcoded string literals (e.g., `"windowUUID"`) in favor of `WindowUUID.userInfo` extension
- Clean up SwiftLint warnings
- Update project file references

## Scope
Affects Redux state management, theming system, coordinators, tab management, settings, and test mocks throughout the codebase.