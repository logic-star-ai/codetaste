# Replace `ReturnErrorCodeIf` with `VerifyOrReturnError`

## Summary
Standardize error handling macros by replacing all uses of `ReturnErrorCodeIf` with `VerifyOrReturnError` and removing the redundant macro definition.

## Why
The codebase has two macros that essentially do the same thing:
- `ReturnErrorCodeIf(expr, value)` - returns `value` if `expr` is true
- `VerifyOrReturnError(expr, value)` - returns `value` if `expr` is false

`VerifyOrReturnError` is:
- More widely used throughout the project
- Better conveys error-handling semantics (verify precondition OR return error)
- Can optionally take extra code as 3rd argument

Having both is redundant and inconsistent.

## Changes
- Convert all `ReturnErrorCodeIf` calls to `VerifyOrReturnError` with inverted conditions
- Apply systematic transformations:
  - `ReturnErrorCodeIf(!$A, $B)` → `VerifyOrReturnError($A, $B)`
  - `ReturnErrorCodeIf($A == $B, $C)` → `VerifyOrReturnError($A != $B, $C)`
  - `ReturnErrorCodeIf($A < $B, $C)` → `VerifyOrReturnError($A >= $B, $C)`
  - ...and other comparison/boolean inversions
- Replace `ReturnErrorCodeWithMetricIf` → `VerifyOrReturnErrorWithMetric`
- Remove `ReturnErrorCodeIf` macro definition from `CodeUtils.h`
- Remove `ReturnErrorCodeWithMetricIf` from metric macros

## Scope
~1000+ occurrences across:
- Platform implementations (ASR, ESP32, Infineon, NXP, Silabs, Telink, Zephyr, Darwin, Android, Linux...)
- Core libraries (app/, credentials/, crypto/, access/, messaging/...)
- Examples (bridge-app, energy-management, chip-tool...)
- Tests