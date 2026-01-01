# Title
-----
Consolidate @ember/object and @ember/object/observable from @ember/-internals/runtime

# Summary
-------
Move `EmberObject`, `FrameworkObject`, and `Observable` mixin from `@ember/-internals/runtime` into their proper public API packages (`@ember/object` and `@ember/object/observable`).

# Why
---
- Better organizational structure by placing implementations in their public API packages
- Reduces number of potential import locations for the same types
- Improves correctness of type exports
- Clearer public API surface

# What Changed
---
**Moved Files:**
- `Observable` mixin: `@ember/-internals/runtime/lib/mixins/observable.ts` → `@ember/object/observable.ts`
- `EmberObject` + `FrameworkObject`: `@ember/-internals/runtime/lib/system/object.ts` → `@ember/object/index.ts`

**Updated Imports:**
- `EmberObject`: `@ember/-internals/runtime` → `@ember/object`
- `Observable`: `@ember/-internals/runtime` → `@ember/object/observable`  
- `FrameworkObject`: `@ember/-internals/runtime` → `@ember/object`

**Removed Exports:**
- `@ember/-internals/runtime/index.ts` no longer exports `Object`, `FrameworkObject`, or `Observable`

**Updated References:**
- Array mixin now imports `Observable` from `@ember/object/observable`
- 100+ test files updated to use new import paths