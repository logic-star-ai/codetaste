# Refactor: Split JmxUtils into Focused Utility Classes

## Summary
`JmxUtils` has grown too large with mixed responsibilities. Extract distinct functionality into separate, well-tested utility classes.

## Why
- **Single Responsibility**: `JmxUtils` handles JSON serialization, string manipulation, numeric validation, and JMX operations
- **Maintainability**: Large utility classes are harder to understand and modify
- **Testability**: Smaller, focused classes are easier to test thoroughly
- **Code Organization**: Related operations should be grouped together

## What Changed
Split `JmxUtils` into:
- **`JsonUtils`**: JSON operations (`getJmxProcess()`, `printJson()`, `prettyPrintJson()`)
- **`NumberUtils`**: Numeric validation (`isNumeric()` methods)
- **`StringUtils`**: String cleanup operations (`cleanupStr()` variants)
- **`JmxUtils`**: Remaining JMX-specific operations

## Implementation Details
- Each new class: `JsonUtils`, `NumberUtils`, `StringUtils`
- All extracted classes have ≥80% line coverage
- Updated ~40 files to use new imports
- Consolidated/reorganized test files
- Added test dependencies: Guava, AssertJ
- Added test resources configuration to `pom.xml`

## Impact
- **Mechanical refactoring**: Method moves with no logic changes
- **Low regression risk**: Behavior preserved, well-tested
- **Breaking change**: Import statements updated throughout codebase

## Notes
Minor import reordering and auto-formatting occurred during extraction.