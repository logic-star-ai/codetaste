# Refactor: Eliminate circular dependencies and dependency injection pattern

## Summary
Complete restructuring of module dependency system across the codebase. Removes dependency injection pattern (modules wrapped in functions receiving dependencies) in favor of explicit CommonJS requires. Eliminates all circular dependencies by establishing proper module boundaries and clear dependency direction.

## Why
- Circular dependencies cause maintenance issues, make code harder to understand, lead to subtle initialization bugs
- Dependency injection via wrapper functions adds unnecessary complexity/indirection
- Cleaner dependency graph enables better tooling (IDE support, static analysis)
- Reduces coupling, makes modules more independently testable
- Establishes foundation for better architecture going forward

## Changes

**Module System**
- Convert ~40 modules from `module.exports = function(tree) { ... }` → direct exports
- Add explicit `require()` at top of each file for actual dependencies
- Remove `tree` parameter passing throughout codebase

**Base Class & Shared Utilities**
- Create `tree/node.js` base class with common functionality (`toCSS`, `genCSS`, `eval`, `_operate`, `fround`)
- All tree nodes now inherit from Node via prototypal inheritance
- Extract `debugInfo` → `tree/debug-info.js`
- Move utility functions off `tree` global object

**Context/Environment**
- Rename and restructure: `tree.parseEnv`/`tree.evalEnv` → `contexts.parseEnv`/`contexts.evalEnv`
- Move to dedicated `env.js` (exposed as `contexts`)
- Update all consumers of parse/eval environments

**Data Organization**  
- Move `tree/unit-conversions.js` → `data/unit-conversions.js`
- Extract colors data → `data/colors.js`
- Centralize static data outside tree structure

**Specific Modules Refactored**
- `tree.js`: Remove wrapper, export flat structure
- All tree/* files: alpha, anonymous, assignment, attribute, call, color, combinator, comment, condition, detached-ruleset, dimension, directive, element, expression, extend, import, javascript, keyword, media, mixin-call, mixin-definition, negative, operation, paren, quoted, rule, ruleset, selector, unicode-descriptor, unit, url, value, variable
- `functions/default.js`, `functions/types.js`: Remove tree dependency
- `parser.js`, `browser.js`: Update to use `contexts` instead of `tree.parseEnv`

## Result
Clean, acyclic dependency graph with explicit module boundaries. No more circular refs, no unnecessary dependency injection scaffolding.