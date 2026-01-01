# Refactor to build with NoFieldSelectors

## Summary
Refactor Stack package to compile with `-XNoFieldSelectors` extension, using `OverloadedRecordDot` syntax for field access. This is a preparatory step for removing prefixes from field names.

## Changes
- Enable `NoFieldSelectors` and `OverloadedRecordDot` extensions throughout codebase
- Replace prefix-based field accessors with dot notation:
  - `prefixFieldName prefix` → `prefix.prefixFieldName`
  - `f prefixFieldName` → `f (.prefixFieldName)`
  - Simplify chains of dots
- Add explicit type annotations where compiler needs help:
  - `Stack.Types.ConfigMonoid` (`mempty :: Map GhcOptionKey GhcOptions`)
  - `Stack.Build.Cache` (`let decode :: MonadIO m => m BuildCache`)
  - `undefined :: <type>` in `defaultBuildOpts`/`defaultTestOpts`

## Why
With `NoFieldSelectors`, record fields no longer generate top-level accessor functions, eliminating the need for prefix-based naming conventions. This enables cleaner field names in a future refactoring.

## Technical Details
- Updated `.hlint.yaml` and `.hlint-test.yaml` configurations
- Adjusted `.stan.toml` line number references
- Systematic transformation across ~100+ files
- Field access patterns: `record.field`, `(.field)`, lens composition with `.`