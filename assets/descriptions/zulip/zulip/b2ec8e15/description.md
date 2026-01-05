# Remove `util` from global scope and convert to proper module

## Summary
Convert `util.js` from a globally-accessible module (`window.util`) to a leaf module that must be explicitly imported via `require()` everywhere it's used.

## Changes

### Core Changes
- Remove `window.util = exports;` from `util.js`
- Remove `util` from `.eslintrc.json` globals list
- Remove `util` from TypeScript `global.d.ts` declarations
- Remove `util` import from `bundles/app.js`

### Import Updates
- Add `const util = require("./util");` to ~40 production files that use util
- Update test files to use `const util = zrequire('util');` instead of implicit global
- Remove unnecessary `zrequire('util')` lines from test files that don't actually use it

## Why
- **Modularity**: Treat util as a proper leaf module with explicit dependencies
- **Clarity**: Make it obvious where util is used vs. assumed to be available
- **Future-proofing**: Preparation for moving util to shared library for mobile code reuse
- **Cleaner dependency graph**: Explicit imports make the codebase easier to understand

## Notes
- Still has one global `blueslip` dependency (to be removed in follow-up commits)
- Considered moving to `shared/` library but deferring that decision
- Module is ~300 lines, will likely move wholesale to shared rather than split up
- When ready to move to shared, will only need simple search/replace on require statements + minor linter tweak