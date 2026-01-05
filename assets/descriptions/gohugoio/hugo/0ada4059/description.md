# Title
-----
Refactor to non-global file systems

# Summary
-------
Eliminate global file system state throughout Hugo by moving to instance-based file systems passed through a dependency structure. This involves creating a new `deps` package to hold shared dependencies and refactoring all file system access to use `*hugofs.Fs` instances instead of global functions.

# Why
---
- Global state makes testing difficult and creates hidden dependencies
- Concurrent operations become safer with isolated file system instances
- Dependency injection makes the codebase more modular and maintainable
- Enables better separation of concerns between different site builds

# Changes Required
---

**Core Infrastructure:**
- Create `deps` package with `Deps` struct containing file systems, logger, templates, and PathSpec
- Move `DepsCfg` from `hugolib` to `deps` package
- Refactor `hugofs` to provide `Fs` struct with `Source`, `Destination`, `Os`, and `WorkingDir` fields
- Replace global `hugofs.Source()`, `hugofs.Destination()`, etc. with instance methods

**Site & Template Changes:**
- Add `*deps.Deps` field to `Site` struct
- Implement `TemplateProvider` interface for template initialization/cloning
- Update template system to accept file system through dependencies
- Remove global template and file system references from template funcs

**Path & Helper Updates:**
- Pass `*hugofs.Fs` to `PathSpec` and helper functions
- Update URL generation and path helpers to use instance-based PathSpec
- Refactor `helpers.CurrentPathSpec()` usage to passed instances

**Test Updates:**
- Update all tests to create `hugofs.NewMem()` or `hugofs.NewDefault()` instances
- Pass file systems explicitly in test helpers
- Remove reliance on `hugofs.InitMemFs()` and similar global initializers

**Command Layer:**
- Create `commandeer` struct holding `deps.DepsCfg` in commands
- Thread file system configuration through command execution
- Update benchmark, server, and build commands to use instance-based deps

# Benefits
---
- Improved testability with isolated file system instances per test
- Better concurrency support for multi-site builds
- Clearer dependency graph and initialization flow
- Easier mocking and testing of file system operations
- Reduced coupling between components