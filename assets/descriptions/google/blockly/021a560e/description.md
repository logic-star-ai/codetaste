# Refactor generator modules to eliminate side effects

## Summary

Restructure generator modules to:
- Move `LangGenerator` class definitions from `generators/lang.js` → `generators/lang/lang_generator.js`
- Move entrypoints from `generators/lang/all.js` → `generators/lang.js`
- Make block generator modules (`generators/lang/*.js`) side-effect-free by exporting individual functions
- Create and configure `langGenerator` instances in the entrypoint files

## Why

Current structure has issues:
- Block generator functions are installed via side effects (direct assignment to generator instance)
- Difficult to load specific generator functions selectively
- Not safe to copy functions between `CodeGenerator` instances
- Poor tree-shaking for projects that build from source

## Changes

### File restructuring
- `generators/{dart,javascript,lua,php,python}.js` → `generators/{lang}/{lang}_generator.js`
  - Contains `{Lang}Generator` class definition only
  - No instance creation
- `generators/{lang}/all.js` → `generators/{lang}.js`
  - Now the entrypoint for `{lang}_compressed.js` chunks
  - Creates `{lang}Generator` instance
  - Calls `.addReservedWords()`
  - Installs all block generator functions via `Object.assign()`

### Block generator modules (`generators/{lang}/*.js`)
- Export individual generator functions (e.g., `export function colour_picker(...)`)
- No direct references to any `CodeGenerator` instance
- Replace `.addReservedWords()` calls with `// RESERVED WORDS: '...'` comments
- Use `export const` aliases for duplicate functions (e.g., `export const controls_ifelse = controls_if`)

### Tests & tooling
- Update `build_tasks.js` chunk entrypoints
- Fix tests importing generators to use `.all` modules where needed
- Update `renamings.json5` to track module path changes

## Benefits

- Projects building from source can pick-and-choose block generators
- Better tree-shaking support
- Cleaner separation of concerns
- Can create multiple generator instances with different configurations
- Sets foundation for exposing individual block generators in published chunks