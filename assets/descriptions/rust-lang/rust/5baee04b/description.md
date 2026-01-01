# Title

Remove `#[macro_use] extern crate tracing` from multiple compiler crates

# Summary

Replace implicit macro imports via `#[macro_use] extern crate tracing` with explicit `use` statements for tracing macros across compiler crates.

# Description

The `#[macro_use]` attribute on `extern crate tracing` is being removed from multiple compiler crates, with explicit imports added at module level instead.

**Affected crates:**
- `rustc_codegen_llvm`
- `rustc_codegen_ssa`
- `rustc_const_eval`
- `rustc_error_messages`
- `rustc_incremental`
- `rustc_interface`
- `rustc_lint`
- `rustc_metadata`
- `rustc_middle`
- `rustc_mir_build`
- `rustc_mir_dataflow`
- `rustc_monomorphize`
- `rustc_parse`
- `rustc_passes`
- `rustc_ty_utils`

**Changes:**
- Remove `#[macro_use] extern crate tracing;` from crate roots
- Add explicit imports like `use tracing::{debug, instrument, trace};` to modules using tracing macros
- Fix incorrect imports (e.g., `use trace;` → `use tracing::trace;`)

**Why:**
Explicit imports via `use` items are more standard, readable, and idiomatic than implicit imports via `#[macro_use]`. This follows modern Rust practices and makes macro usage more discoverable.