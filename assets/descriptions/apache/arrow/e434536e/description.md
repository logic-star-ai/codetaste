# Refactor compute test utilities and reorganize Grouper tests

## Summary
Move Grouper/RowSegmenter tests to proper location, consolidate duplicate test utilities, and introduce `arrow_compute_testing` object library for shared testing infrastructure.

## Why
- Grouper and RowSegmenter tests located in `acero/hash_aggregate_test.cc` instead of `compute/row/grouper_test.cc`
- Duplicate `ExecBatchFromJSON` implementations in Dataset and Acero modules
- Test utility header `arrow/compute/kernels/test_util.h` exposed publicly when it should be internal-only
- No centralized object library for compute-related testing utilities

## Changes
- Move all Grouper/RowSegmenter tests from `acero/hash_aggregate_test.cc` → `compute/row/grouper_test.cc` (~900 lines)
- Create `arrow_compute_testing` object library containing:
  - `test_util_internal.cc/h` with `ExecBatchFromJSON`, `ValidateOutput`, `ArgShape` enum
- Rename `compute/kernels/test_util.{h,cc}` → `test_util_internal.{h,cc}`
- Remove duplicate `ExecBatchFromJSON` from:
  - `acero/test_util_internal.{h,cc}`
  - `dataset/test_util_internal.{h,cc}`
- Update CMakeLists.txt to link `arrow_compute_testing` in tests
- Update all import statements across kernels/acero/dataset test files

## Benefits
- Tests properly organized by module
- Single source of truth for common test utilities
- Cleaner internal vs. public API boundaries
- Shorter `hash_aggregate_test.cc` file