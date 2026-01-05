# Refactor route functions in BaseService

## Summary

Extract route helper functions (`_makeFullUrl`, `_regex`, `_regexFromPath`, `_namedParamsForMatch`) from BaseService into standalone, testable functions in new `route.js` module.

## Why

- Route helpers are well-isolated from rest of BaseService → easier to test independently
- `pathToRegexp` currently invoked once per request → inefficient
- Route validation happens at usage time → should validate upfront during registration

## Changes

**Extract to new `core/base-service/route.js`:**
- `makeFullUrl(base, partialUrl)` (formerly `_makeFullUrl`)
- `assertValidRoute(route, message)` (new - validates route schema)
- `prepareRoute({ base, pattern, format, capture })` (formerly `_regex` + `_regexFromPath` - pre-computes regex)
- `namedParamsForMatch(captureNames, match, ServiceClass)` (formerly `_namedParamsForMatch`)

**Update BaseService & subclasses:**
- Use new helpers in `base.js`, `base-static.js`, `base-non-memory-caching.js`
- Call `prepareRoute()` once during registration instead of per request
- Add upfront route validation via `assertValidRoute()`

**Fix services missing patterns:**
- Add `pattern: ''` to ~30+ services to pass new validation
- Move `pattern` from examples to route definition where misplaced

**Tests:**
- Move route tests from `base.spec.js` to new `route.spec.js`
- Update test fixtures with valid route definitions

## Benefits

- ✅ Better testability & separation of concerns
- ✅ Performance: pathToRegexp computed once vs. per request
- ✅ Fail fast: route validation at registration vs. first use