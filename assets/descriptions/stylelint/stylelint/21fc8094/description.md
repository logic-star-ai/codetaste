# Title
Migrate medium utility modules to ESM

# Summary
Migrate utility modules to ES Modules format while maintaining CommonJS compatibility through dual `.cjs`/`.mjs` outputs. Optimize Rollup configuration to eliminate redundant helpers and symbols from generated bundles.

# Changes

## Utility Modules Migrated
- `checkInvalidCLIOptions` → `.cjs` + `.mjs`
- `configurationComment` → `.cjs` + `.mjs`
- `filterFilePaths` → `.cjs` + `.mjs`
- `findMediaFeatureNames` → `.cjs` + `.mjs`
- `getCacheFile` → `.cjs` + `.mjs`
- `hash` → `.cjs` + `.mjs`
- `hasInterpolation` → `.cjs` + `.mjs`
- `isAfterStandardPropertyDeclaration` → `.cjs` + `.mjs`
- `isStandardSyntax*` family (AtRule, ColorFunction, Combinator, Comment, Declaration, Function, HexColor, KeyframesName, Property, Rule, Selector, Url, Value) → `.cjs` + `.mjs`
- `parseSelector` → `.cjs` + `.mjs`
- `transformSelector` → `.cjs` + `.mjs`

## Module Format Updates
- `.cjs` files: Pure CommonJS (`require()`, `module.exports`)
- `.mjs` files: Pure ESM (`import`, `export default`, named exports)
- Update all imports throughout codebase to reference correct extensions

## Rollup Configuration
Configure output options to optimize bundle:
- `output.interop: 'default'` - Remove unnecessary interop helpers
- `output.esModule: false` - Remove `__esModule` flag from CJS output
- `output.generatedCode.symbols: false` - Eliminate unneeded Symbol helpers (e.g., `Symbol.toStringTag`)

## Cleanup
- Remove `_interopDefault` helper functions from generated output
- Remove `Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' })` from CJS files
- Update test imports to use `.mjs` extensions

# Related
Ref #5291