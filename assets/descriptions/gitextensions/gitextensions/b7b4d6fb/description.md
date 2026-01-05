# Rename `GitCommandHelpers` to `Commands` and simplify method names

## Summary
Refactor `GitCommandHelpers` class to `Commands` and remove redundant `Cmd` suffix from all method names.

## Changes

### Type Rename
- `GitCommandHelpers` → `Commands` (now partial class)
- `GitCommandHelpers.cs` → `Commands.Arguments.cs`

### Method Renames (remove `Cmd` suffix)
- `CherryPickCmd` → `CherryPick`
- `SubmoduleUpdateCmd` → `SubmoduleUpdate`
- `SubmoduleSyncCmd` → `SubmoduleSync`
- `AddSubmoduleCmd` → `AddSubmodule`
- `GetCurrentChangesCmd` → `GetCurrentChanges`
- `GetRefsCmd` → `GetRefs`
- `RevertCmd` → `Revert`
- `ResetCmd` → `Reset`
- `PushLocalCmd` → `PushLocal`
- `CloneCmd` → `Clone`
- `CheckoutCmd` → `Checkout`
- `CreateOrphanCmd` → `CreateOrphan`
- `RemoveCmd` → `Remove`
- `BranchCmd` → `Branch`
- `MergedBranchesCmd` → `MergedBranches`
- `PushMultipleCmd` → `PushMultiple`
- `PushTagCmd` → `PushTag`
- `StashSaveCmd` → `StashSave`
- `Continue/Skip/Abort/Start/Stop...Cmd` → `Continue/Skip/Abort/Start/Stop...`
- `...Cmd` → `...` (all other methods follow same pattern)

### Affected Areas
- `GitCommands/Git/...`
- `GitUI/CommandsDialogs/...`
- `GitUI/UserControls/...`
- `UnitTests/...`
- Documentation/comments

## Why

**Improved naming clarity**: `Commands.CherryPick()` is cleaner and more idiomatic than `GitCommandHelpers.CherryPickCmd()`

**Reduced redundancy**: The `Cmd` suffix is unnecessary when the class is already named `Commands`

**Better organization**: Making the class `partial` allows for better file organization