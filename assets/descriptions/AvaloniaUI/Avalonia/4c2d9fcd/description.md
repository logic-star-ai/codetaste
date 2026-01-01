# Refactor IntegrationTestApp paging system

## Summary

Replace `TabControl`-based navigation with `ListBox` pager in IntegrationTestApp. Extract tab content into separate page controls and centralize page selection logic in test base class.

## Why

- Current `TabControl` layout breaks on small screens (integration tests run at very small resolutions)
- Adding "Embedding" tab caused tabs to expand to 3 columns, leaving minimal room for content
- All tab definitions in single `MainWindow.xaml` file becoming unwieldy and hard to maintain
- Tests needed refactoring to handle potential scrolling requirements

## Changes

**IntegrationTestApp Structure:**
- Replace `TabControl` with `ListBox` for page navigation (prevents horizontal tab growth)
- Extract each tab's content into separate `UserControl` files:
  - `AutomationPage.axaml`, `ButtonPage.axaml`, `CheckBoxPage.axaml`, etc.
  - Move associated logic from `MainWindow.axaml.cs` into respective page code-behinds
- Create `Page` model: `record Page(string Name, Func<Control> CreateContent)`
- Add MVVM structure:
  - `MainWindowViewModel` with `Pages` collection and `SelectedPage` property
  - `ViewModelBase` with `INotifyPropertyChanged` implementation
- Simplify `MainWindow.axaml`:
  - `ListBox` (Pager) on left with page names
  - `Decorator` (PagerContent) for displaying selected page content

**Test Infrastructure:**
- Create `TestBase` class with page selection logic in constructor
  - Takes `pageName` parameter, finds and clicks corresponding page
  - Includes retry logic for macOS timing issues
  - Exposes `Session` property for derived tests
- Update all test classes to inherit from `TestBase` instead of manually selecting tabs:
  - `AutomationTests`, `ButtonTests`, `CheckBoxTests`, `ComboBoxTests`, etc.
- Remove duplicate tab selection code from individual test classes

**Automation Support:**
- Add `AutomationPeer.IsOffscreen()` method and `IsOffscreenCore()` virtual
- Add `IsOffscreenBehavior` enum to `AutomationProperties` (Onscreen/Offscreen/FromClip/Default)
- Override `IsOffscreenBehavior` default for controls that can be scrolled offscreen:
  - `DataGridCell`, `DataGridColumnHeader`, `DataGridRow`, `DataGridRowHeader`
  - `ListBoxItem`, `MenuItem`, `TabItem`, `TreeViewItem`
- Implement `IsOffscreen` property in Windows UIA (`AutomationNode.cs`)
- Default behavior: check if control is clipped or invisible

## Implementation Notes

- `ListBox` with vertical `StackPanel` ensures pages remain accessible regardless of count
- Page factory pattern (`Func<Control>`) allows lazy instantiation
- Test base class prepares for future macOS scrolling requirements (Appium doesn't auto-scroll on macOS)
- `IsOffscreen` implementation matches WPF behavior and enables WinAppDriver element scrolling