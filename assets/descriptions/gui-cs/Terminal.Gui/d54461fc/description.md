# Rename `Frame` to `Adornment` and Create Border/Margin/Padding Subclasses

## Summary
Refactor the `Frame` class to `Adornment` with specialized `Border`, `Margin`, and `Padding` subclasses. Improve border inheritance and LineStyle management.

## Changes

### Core Refactoring
- Rename `Frame` class → `Adornment` class
- Create `Border : Adornment` subclass with `LineStyle` property
- Create `Margin : Adornment` subclass  
- Create `Padding : Adornment` subclass
- Move `Border`-specific logic from `Frame.OnDrawContent` to `Border.OnDrawContent`

### API Changes
- `View.CreateFrames()` → `View.CreateAdornment(Type)`
- `View.LayoutFrames()` → `View.LayoutAdornments()`
- `View.OnDrawFrames()` → `View.OnDrawAdornments()`
- `View.GetFramesThickness()` → `View.GetAdornmentsThickness()`
- `Frame.BorderStyle` → `Border.LineStyle`

### Color Scheme Inheritance
- `Border.ColorScheme` inherits from `Parent.ColorScheme` if not set
- `Margin.ColorScheme` inherits from `Parent.SuperView.ColorScheme` if not set
- `Padding.ColorScheme` inherits from `Parent.ColorScheme` if not set

### Border Title Rendering
- Improve title rendering for `Border.Thickness.Top` values of 0, 1, 2, 3+
- Title now uses `GetFocusColor()` when parent `HasFocus`

### Test Infrastructure
- Rename `TestHelpers.AssertDriverColorsAre()` → `AssertDriverAttributesAre()`
- Add `TestHelpers.DriverContentsToString()` helper
- Improve `Cell.ToString()` and `Attribute.ToString()` for debugging

### Scenarios
- Rename `Frames.cs` → `Adornments.cs` scenario
- Rename `FramesEditor` → `AdornmentsEditor`
- Rename `FrameEditor` → `AdornmentEditor`

### Documentation
- Update XML docs to reference `Adornment` instead of `Frame`
- Update comments referencing frames/borders

## Why
- "Adornment" is clearer terminology for margins/borders/padding
- Subclasses provide better type safety and code organization
- Border can now properly inherit `LineStyle` from SuperView hierarchy
- Separates concerns between generic adornment logic and border-specific rendering