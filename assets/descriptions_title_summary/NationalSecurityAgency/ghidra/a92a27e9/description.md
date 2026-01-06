# Refactor GUI theme management to use ThemeManager pattern

Refactor the `Gui` class from a monolithic static utility to a proper ThemeManager-based architecture. Move all theme management logic from static `Gui` methods into instance methods of `ThemeManager`, `ApplicationThemeManager`, and `StubThemeManager` classes.