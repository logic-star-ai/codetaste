# Refactor Host Config Infrastructure: Remove `.inline*.js` Files

## Summary

Remove all `.inline*.js` entry point files across reconciler packages (`react-reconciler`, `react-server`, `react-flight`) and replace with direct imports to source files. Update Flow configuration to use explicit path-based type checking strategy.

## Why

The `.inline*.js` indirection made it confusing to understand the renderer architecture. Hard to remember what each inline file does, difficult to add new combinations. 

Untyped inline files caused "any" types to leak throughout the system once they entered — insufficient approach that required hacks. Uncertainty about which files were typed vs untyped.

## Changes

**Imports**
- All renderers now import directly: `'react-reconciler/src/ReactFiberReconciler'` instead of `'react-reconciler/inline.dom'`, etc.
- Same pattern for `react-server/src/*` and `react-flight/src/*`

**Deleted Files**
- All `.inline*.js` files: `inline.dom.js`, `inline.art.js`, `inline.fabric.js`, `inline.native.js`, `inline.test.js`, ...
- All `inline-typed.js` files
- `react-reconciler/persistent` entry point (no longer makes sense — reconciler takes `supportsMutation`/`supportsPersistence` as options now, not feature flags)

**Flow Strategy**
- No more untyped files → no need for `inline-typed` form
- Each renderer now explicitly selects which paths to check
- Inverse paths get ignored (not untyped!)
- Every path still covered by *some* renderer
- If dependency accidentally reaches uncovered code → error, not silent "any" leak

**Jest Mocking**
- Updated `setupHostConfigs.js` to mock host configs at actual entry points instead of inline files
- Removed `react-reconciler/persistent` mock

**Config Changes**
- Added explicit `paths` array to each renderer in `inlinedHostConfigs.js`
- Flow config now generates renderer-specific ignore patterns based on paths

## Benefits

- Clearer architecture — actual renderer entry points are the hooks, not pseudo entry points
- No untyped "any" leaks
- Stronger type safety — accidental imports are errors, not silent failures
- Easier to add new renderer combinations
- Consistent with how we already handle other deep requires