# Migrate `rustc_incremental` diagnostics to translatable structs

## Summary

Migrate diagnostics in `rustc_incremental` crate from string-based errors to translatable diagnostic structs. Apply diagnostic migration lints to additional `Session` methods and add `IntoDiagnosticArg` implementations for common types.

## Changes

### Core Migration
- Create `compiler/rustc_incremental/src/errors.rs` with ~50 diagnostic structs
- Add fluent messages in `compiler/rustc_error_messages/locales/en-US/incremental.ftl`
- Replace all `sess.err()`, `sess.warn()`, `sess.span_err()`, etc. calls with `emit_err()`, `emit_warning()`, etc.
- Update modules: `assert_dep_graph.rs`, `assert_module_sources.rs`, `dirty_clean.rs`, `file_format.rs`, `fs.rs`, `load.rs`, `save.rs`, `work_product.rs`

### Session Lint Coverage
Apply `#[rustc_lint_diagnostics]` to additional `Session` methods:
- `span_warn`, `span_warn_with_code`, `warn`
- `note_without_error`, `span_note_without_error`, `struct_note_without_error`

### IntoDiagnosticArg Implementations
Add implementations for:
- `std::io::Error`
- `std::path::Path` / `std::path::PathBuf`
- `std::ffi::CString`
- `rustc_data_structures::small_c_str::SmallCStr`

### Side Migrations
Also migrate diagnostics in:
- `rustc_codegen_llvm` (LTO, write operations)
- `rustc_driver` (ICE reporting)
- `rustc_interface`, `rustc_monomorphize`, `rustc_passes`, `rustc_expand`

### Feature Flags
Enable `#![feature(never_type)]` for diagnostic return types
Add lints: `#![deny(rustc::untranslatable_diagnostic)]`, `#![deny(rustc::diagnostic_outside_of_impl)]`

## Why

- **i18n**: Enables proper internationalization of compiler diagnostics
- **Type Safety**: Structured diagnostics prevent runtime formatting errors
- **Consistency**: Aligns with diagnostic migration effort across compiler crates
- **Tooling**: Enables future diagnostic tooling and analysis