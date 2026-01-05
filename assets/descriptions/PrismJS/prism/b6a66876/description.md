# Remove redundant `prism-` prefix from plugin filenames

## Summary

Plugin files currently use `prism-{id}.js` / `prism-{id}.css` naming (e.g., `prism-autoloader.js`, `prism-toolbar.css`). This should be simplified to `{id}.js` / `{id}.css` to align with language and theme naming conventions.

## Why

- Languages use `{id}.js` (not `prism-{id}.js`)
- Themes use `{id}.css` (not `prism-{id}.css`)
- Plugin naming is inconsistent with the rest of the codebase
- The `prism-` prefix is redundant (files are already in `plugins/` directory)

## Changes

**File renames:**
- `plugins/{id}/prism-{id}.js` → `plugins/{id}/{id}.js`
- `plugins/{id}/prism-{id}.css` → `plugins/{id}/{id}.css`

**Update imports:**
- All plugin-to-plugin imports (toolbar, autoloader, custom-class, ...)
- `auto-start.js` autoloader import

**Update references:**
- `components.json` path pattern
- `package.json` exports (add `./plugins/*` rule)
- Build scripts (`build.js`, `create-changelog.js`)
- Test helpers (`prism-loader.js`)
- Plugin documentation and examples (README files, demo pages)
- JSDoc `@typedef` import paths

## Scope

All 24 plugins + their CSS files where applicable. No functional changes—purely file renames and path updates.