# Refactor element visibility handling: standardize on `.gt-hidden` and helper functions

Unify element hiding/showing mechanisms across the codebase by:
- Introducing `.gt-hidden` class with `display: none !important`
- Creating `showElem()`, `hideElem()`, `toggleElem()` helper functions in `utils/dom.js`
- Removing jQuery's `.show()`, `.hide()`, `.toggle()` methods
- Replacing `.hide` class with `.gt-hidden`
- Removing inline `style="display:none"` attributes