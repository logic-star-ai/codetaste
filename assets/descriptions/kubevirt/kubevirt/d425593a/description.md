# Title

Move migration tests to dedicated package

# Summary

Refactor migration tests from single monolithic `migration_test.go` file into a new `tests/migration` package with better organization and helper libraries.

# Why

`migration_test.go` had grown significantly over time, causing:
- **Readability issues**: Large file (4000+ lines) difficult to navigate and understand
- **Maintainability problems**: Overlapping `Context` blocks, unclear test organization
- **Flakiness**: Recent test flakes due to complex setup and intertwined code
- **Code smell**: Helper functions mixed with tests, unclear separation of concerns

# What Changed

## Package Structure

- **Created** `tests/migration/` package:
  - `migration.go` - Core migration test suite
  - `migration_policy.go` - Migration policy test helpers
  - `framework.go` - Test framework utilities (SIGMigrationDescribe, etc.)

- **Created** `tests/libmigration/` library package:
  - Extracted reusable migration helpers from `tests/migration.go`:
    - `ExpectMigrationToSucceed*()`
    - `RunMigration*()` functions
    - `ConfirmVMIPostMigration()`
    - `ConfirmVMIPostMigrationAborted()`
    - Migration network setup (SetDedicatedMigrationNetwork, etc.)
    - Migration metrics collection
    - ... and more

## Test Code Cleanup

- **Moved** node-labeller helpers to `tests/libinfra/node-labeller.go`:
  - `ExpectStoppingNodeLabellerToSucceed()`
  - `ExpectResumingNodeLabellerToSucceed()`

- **Consolidated** VMI factory functions:
  - Merged `NewRandomFedoraVMI*` variants into single function with options
  - Created `libvmi.NewWindows()` for Windows VMI creation
  - Added `WithEphemeralPersistentVolumeClaim()` option

- **Removed** errcheck exception for migration_test.go in nogo_config.json

## Import Updates

Updated ~30 test files to import from new packages:
- `kubevirt.io/kubevirt/tests/libmigration`
- `kubevirt.io/kubevirt/tests/migration`

# Benefits

- Modular code organization enables future test file splitting
- Clear separation between test code and helper libraries
- Improved discoverability of migration-related utilities
- Foundation for further migration test refactoring
- Better maintainability and reduced flake potential