# Improve Error Handling with Explicit Error Types

## Summary
Replace `anyhow` with `thiserror` to provide more explicit and traceable error messages throughout the CLI and bundler crates.

## Why
- Difficult to trace errors when building apps (e.g., vague "directory not empty" errors)
- Generic errors don't provide enough context about what actually failed
- Need more explicit error variants for better debugging

## What Changed
- **Dropped `anyhow`** from `tauri-cli` and `tauri-bundler`
- **Added `thiserror`** for structured error types
- Created custom `Error` enum with variants like:
  - `Fs { context, path, error }` - Filesystem operations with path context
  - `CommandFailed { command, error }` - Failed command execution
  - `Context(String, Box<Error>)` - Error with additional context
  - Platform-specific variants (e.g., `AppleCodesign`, `AppleNotarization`)
- **Implemented `Context` trait** - Similar to `anyhow::Context` for adding context to errors
- **Added `ErrorExt` trait** - `fs_context` helper for filesystem operations
- Updated all error handling to use explicit context

## Examples
```rust
// Before
std::fs::remove_dir_all(&path)?;

// After  
std::fs::remove_dir_all(&path)
  .fs_context("failed to remove old package directory", path.clone())?;
```

## Notes
- Kept anyhow-style context chaining
- Some technical debt remains in bundler error type
- Changes are verbose but provide much better error messages