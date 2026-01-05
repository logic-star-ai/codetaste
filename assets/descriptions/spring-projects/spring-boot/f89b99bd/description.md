# Title

Refactor ConfigData processing to clarify location vs resource concepts

## Summary

ConfigData processing code uses confusing terminology where "location" refers to both String values and typed instances, making the code awkward to follow with no proper home for `optional:` prefix logic and Origin support.

## Why

- `location` ambiguously means both String value and typed instance
- `optional:` prefix handling scattered across codebase (passed as boolean parameters)
- Origin tracking lacks proper integration
- `ResourceConfigData...` naming unclear

## Changes

**Core Refactoring:**
- Rename `ConfigDataLocation` → `ConfigDataResource` (resolved, typed resource)
- Create new `ConfigDataLocation` class wrapping String value with:
  - `optional:` prefix handling (`isOptional()`, `getValue()`, `getNonPrefixedValue()`)
  - Origin tracking
  - Prefix checking utilities

**Exception Hierarchy:**
- Introduce base `ConfigDataNotFoundException`
- `ConfigDataLocationNotFoundException` - location resolution failures
- `ConfigDataResourceNotFoundException` - resource loading failures

**Naming Cleanup:**
- `ResourceConfigData...` → `StandardConfigData...`
- `ConfigDataLocationNotFoundAction` → `ConfigDataNotFoundAction`
- `spring.config.on-location-not-found` → `spring.config.on-not-found`

**Simplifications:**
- Remove `OptionalConfigDataLocation` wrapper class
- Remove boolean `optional` parameters from method signatures
- Consolidate location resolution/loading logic