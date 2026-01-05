# Refactor element visibility handling: standardize on `.gt-hidden` and helper functions

## Summary

Unify element hiding/showing mechanisms across the codebase by:
- Introducing `.gt-hidden` class with `display: none !important`
- Creating `showElem()`, `hideElem()`, `toggleElem()` helper functions in `utils/dom.js`
- Removing jQuery's `.show()`, `.hide()`, `.toggle()` methods
- Replacing `.hide` class with `.gt-hidden`
- Removing inline `style="display:none"` attributes

## Why

Multiple conflicting visibility mechanisms cause issues:
- `[hidden]` attribute: too weak, doesn't work with `display: flex`
- `.hidden` class: polluted by Fomantic UI
- `.hide` class: inconsistent
- Inline `style="display:none"`: hard to maintain
- jQuery's `show()`/`hide()`: doesn't work with `!important` styles

## Changes

### New utilities (`web_src/js/utils/dom.js`)
```js
showElem(el)   // removes .gt-hidden
hideElem(el)   // adds .gt-hidden  
toggleElem(el, force?) // toggles .gt-hidden
```

### Template changes
- Replace `.hide` → `.gt-hidden`
- Replace `style="display:none"` → `class="gt-hidden"`
- Update `...` occurrences across admin/*, repo/*, user/*, org/*, install.tmpl, etc.

### JavaScript changes
- Replace `$el.show()` → `showElem($el)`
- Replace `$el.hide()` → `hideElem($el)`
- Replace `$el.toggle()` → `toggleElem($el)`
- Update files: features/*, components/*

### CSS
- Add `.gt-hidden { display: none !important; }` in helpers.less
- Remove `.hide` from _base.less

### Linting
- Enable ESLint rules: `jquery/no-hide`, `jquery/no-show`, `jquery/no-toggle`

## Documentation

Add guidelines in `docs/.../guidelines-frontend.md`:
- ✅ Use: `.gt-hidden` class + `showElem()`/`hideElem()`/`toggleElem()`
- ❌ Don't use: `[hidden]`, `.hidden`, `.hide`, inline styles, jQuery methods