# Refactor `dev().assert` to `devAssert`

Replace all `dev().assert(...)` calls with standalone `devAssert(...)` function across the codebase.

## Summary

Systematically replace ~500+ instances of `dev().assert(...)` with `devAssert(...)` throughout the repository and make the old usage illegal via presubmit check.

## Why

- **Type inference broken with `dev().assert(...)`** - Type checkers (TypeScript/Flow) cannot properly narrow types when assertion is called through method chaining
- **`devAssert(...)` enables proper type narrowing** - Standalone function allows type checkers to understand asserted condition is truthy
- **Cleaner, more consistent API** - Shorter syntax, enforced via presubmit checks

## Implementation

- Replace all `dev().assert(...)` → `devAssert(...)`  
- Update imports: `import {dev, devAssert} from './log'` or `import {devAssert} from './log'`
- Add presubmit check forbidding `dev\(\)\.assert\(` pattern (whitelist: `src/log.js`)
- `devAssert()` implementation in `src/log.js` internally calls `dev()./*Orig call*/assert(...)`
- No behavior change in minified mode

## Files Changed

- `3p/*.js` - ... 
- `ads/**/*.js` - ...
- `extensions/**/*.js` - ...
- `src/**/*.js` - ...
- `build-system/tasks/presubmit-checks.js` - Added enforcement rule

## Follow-up

Does **not** remove unnecessary type casts that were previously needed due to poor type inference. Those will be cleaned up separately.