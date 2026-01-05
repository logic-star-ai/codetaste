# Reorganize `run-make-support` library into focused modules

## Summary

Break up monolithic `lib.rs` into smaller, functionally-organized modules to improve discoverability and reduce cognitive overhead when working with the `run-make-support` library.

## Why

The current `run-make-support/lib.rs` is a kitchen sink containing ~650 lines of mixed functionality, making it difficult to:
- Discover available helpers
- Understand module organization
- Locate specific functionality
- Learn the API surface

## Changes

### Module Structure

Create focused modules:
- `artifact_names.rs` - helpers for constructing target-dependent artifact names (`static_lib_name`, `dynamic_lib_name`, `bin_name`, etc.)
- `assertion_helpers.rs` - assertion utilities (`assert_equals`, `assert_contains`, `assert_dirs_are_equal`, etc.)
- `env.rs` - environment variable accessors with panic-on-fail semantics
- `external_deps/` - external tool wrappers organized by tool:
  - `cc.rs`, `clang.rs`, `llvm.rs`, `python.rs`, `rustc.rs`, `rustdoc.rs`, `htmldocck.rs`
  - `c_build.rs` - higher-level build helpers
  - `cygpath.rs` - internal dependency
- `fs.rs` - filesystem operations (replaces `fs_wrapper`, re-exported as `rfs` to avoid confusion with `std::fs`)
- `macros.rs` - internal macro definitions (`impl_common_helpers!`)
- `path_helpers.rs` - path manipulation and discovery utilities
- `scoped_run.rs` - test execution with maintained properties (`run_in_tmpdir`, `test_while_readonly`)
- `string.rs` - string/text matching helpers
- `targets.rs` - target detection predicates
- `util.rs` - internal utilities

### Renames

- `recursive_diff` → `assert_dirs_are_equal` (more descriptive)
- `read_dir` (callback variant) → `read_dir_entries` (disambiguate from `std::fs::read_dir`)
- `fs_wrapper` module → `fs` module, re-exported as `rfs` to tests

### `lib.rs` Simplification

Transform `lib.rs` from implementation to organized re-export surface:
- Third-party library re-exports
- Grouped re-exports by functionality
- Clear public API with module documentation

### Test Updates

Update all ~100+ run-make tests to use new import paths:
- `fs_wrapper::` → `rfs::`
- Direct function imports from appropriate modules

## Benefits

- **Discoverability**: Related functionality grouped together
- **Clarity**: Module names indicate purpose
- **Maintainability**: Smaller files, focused responsibilities
- **Documentation**: Easier to document cohesive modules
- **Precedent**: Foundation for future documentation improvements