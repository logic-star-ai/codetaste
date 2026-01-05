# Rename `wasi` crate to `wasip1` in test-programs

## Summary

Rename the `wasi` crate import to `wasip1` throughout test-programs to explicitly indicate WASI Preview 1.

## Why

Test programs currently have access to both WASI preview1 and preview2 versions. Using the generic name `wasi` creates ambiguity about which version is being used. Renaming to `wasip1` provides clear disambiguation.

## What Changed

- **Cargo.toml**: Changed dependency from `wasi = "0.11.0"` to `wasip1 = { version = "0.11.0", package = 'wasi' }`
- **All test binaries**: Updated all `wasi::*` references to `wasip1::*` across:
  - Type references (`wasi::Fd` → `wasip1::Fd`)
  - Function calls (`wasi::fd_close()` → `wasip1::fd_close()`)
  - Constants (`wasi::ERRNO_BADF` → `wasip1::ERRNO_BADF`)
  - Structs (`wasi::Iovec` → `wasip1::Iovec`)

## Scope

- `crates/test-programs/Cargo.toml`
- `crates/test-programs/src/bin/*.rs` (all preview1 test programs)
- `crates/test-programs/src/preview1.rs` (helper functions)