# Title
-----
Restructure `frame_support` macro-related exports to `__private` module

# Summary
-------
Restructure `frame_support`'s public API by moving macro-related reexports to a private `__private` module, forcing explicit imports and clarifying what constitutes public vs internal API surface.

# Why
---
- Clean separation between public API and internal macro implementation details
- Prevent reliance on transitive exports through `frame_support`
- Make dependencies explicit in pallet code
- Reduce API surface and improve maintainability

# Changes
---------

**frame_support exports:**
- Create new `__private` module containing:
  - `codec`, `scale_info`, `log`, `paste`, `serde`
  - `sp_std`, `sp_io`, `sp_runtime`, `sp_core`, `sp_tracing`
  - `metadata`, `metadata_ir`, `BasicExternalities`
  - `RuntimeDebug`, `OpaqueMetadata`, `Void`
  - `tt_call` macros
- Remove these from public reexports

**Macro code generation:**
- Update all procedural macros to use `#frame_support::__private::` paths:
  - `construct_runtime` (call, config, metadata, origin, outer_enums, etc.)
  - `#[pallet]` macros (call, event, error, storage, etc.)
  - `#[benchmark]` macros
  - Storage alias macros

**Pallet updates:**
- Add explicit imports for `codec`, `log`, `scale_info`, `RuntimeDebug`
- Import from `sp_runtime`, `sp_std`, `sp_io` directly
- Update `Cargo.toml` dependencies where needed
- Replace `frame_support::bounded_vec` → `sp_runtime::bounded_vec`
- Replace `frame_support::RuntimeDebug` → `sp_runtime::RuntimeDebug`
- Replace `frame_support::metadata_ir` → `sp_metadata_ir`

**Test updates:**
- Update UI tests for new import paths
- Fix compilation errors from changed exports

# Scope
------
Affects:
- `frame/support/` (core changes)
- `frame/*/` (all pallets)
- `bin/node/runtime/`
- Test and benchmark code

# Breaking
----------
⚠️ Breaking change for external pallet authors who relied on transitive exports through `frame_support`