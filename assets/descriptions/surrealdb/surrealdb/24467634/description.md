# Remove `include!` usage from tests

## Summary

Refactor test suite to eliminate `include!` macro usage, replacing with proper module structure and macros for test instantiation across multiple backend configurations.

## Why

Using `include!` for test definitions has significant drawbacks:
- Bypasses normal Rust module system
- Unhygienic, causes tooling issues
- Introduces unnecessary code duplication for compiler
- Makes tests harder to maintain and debug

## Changes

**Test Organization:**
- Convert test files from `include!` targets → proper modules with public functions
- Introduce `CreateTx`/`CreateDs` traits for backend-agnostic test setup
- Use `define_tests!` macros to generate test functions that delegate to module functions
- Each backend (mem, rocksdb, tikv, fdb, surrealkv, ws, http) instantiates tests via `include_tests!` macro

**Test Quality:**
- Replace `assert!(...is_ok())` → `.unwrap()` so errors actually print the error value
- Better error visibility when tests fail

**CI Fixes:**
- Fix `kvs` tests not actually running (wrong package name in Makefile)
- Add `clear-fdb` task to reset FoundationDB state between test runs
- Fix TiKv test cleanup (use `delr` instead of `delp`)

**Affected Areas:**
- `crates/core/src/kvs/tests/*` - KV store backend tests
- `tests/ws_integration.rs` - WebSocket integration tests  
- `crates/sdk/tests/api*.rs` - SDK API tests
- Various unit tests with `assert!(...is_ok())` patterns

## Structure

```
kvs/tests/
├── mod.rs          # Traits + macro orchestration
├── raw.rs          # define_tests! macro + test fns
├── snapshot.rs     # ...
├── multireader.rs  # ...
└── ...

Each backend module:
- Calls `include_tests!(new_ds, new_tx => test1, test2, ...)`
- Macro generates #[test] functions calling `super::module::test_fn(new_ds)`
```