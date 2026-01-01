# Replace failure `Category` raw strings with typed constants

## Summary
Introduce `FailureCategory` type and replace all raw string literals used for failure categories throughout the codebase with typed constants.

## Why
- **Type Safety**: Raw strings are error-prone and allow typos/inconsistencies
- **Discoverability**: Constants enable better IDE autocomplete/navigation
- **Maintainability**: Centralized definitions make category management easier
- **Refactoring**: Future category consolidation (e.g., merging `FailureCategoryCodeStyle` and `FailureCategoryStyle`) becomes simpler

## Changes
- Add `type FailureCategory string` in `lint/failure.go`
- Define constants for all categories:
  - `FailureCategoryArgOrder`, `FailureCategoryBadPractice`, `FailureCategoryCodeStyle`, `FailureCategoryComments`, `FailureCategoryComplexity`, `FailureCategoryContent`, `FailureCategoryErrors`, `FailureCategoryImports`, `FailureCategoryLogic`, `FailureCategoryMaintenance`, `FailureCategoryNaming`, `FailureCategoryOptimization`, `FailureCategoryStyle`, `FailureCategoryTime`, `FailureCategoryTypeInference`, `FailureCategoryUnaryOp`, `FailureCategoryUnexportedTypeInAPI`, `FailureCategoryZeroValue`
  - Internal: `failureCategoryInternal`, `failureCategoryValidity`
- Update `Failure.Category` field from `string` to `FailureCategory`
- Replace all raw string literals (`"style"`, `"naming"`, `"logic"`, ...) with respective constants across ~50 rule files