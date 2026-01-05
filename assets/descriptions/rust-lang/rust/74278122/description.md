Title
-----
Remove `#[macro_use] extern crate` declarations for explicit imports

Summary
-------
Replace implicit macro imports via `#[macro_use] extern crate foo` with explicit `use` statements throughout the compiler codebase. This makes the code more verbose but significantly improves readability by making it clear where macros and types are defined.

Why
---
- `#[macro_use]` obscures where macros are defined, requiring developers to search or guess
- Explicit imports provide better locality and clarity
- Easier to understand dependencies and trace macro origins

Changes
-------
**Removed `#[macro_use] extern crate` for:**
- `rustc_macros` 
- `rustc_middle`
- `rustc_data_structures`
- `tracing`
- `bitflags`
- `smallvec`
- `scoped_tls`

**Added explicit `use` statements for:**
- Derive macros: `Decodable`, `Encodable`, `HashStable_Generic`, `TypeFoldable`, `TypeVisitable`, etc.
- Helper macros: `bug`, `span_bug`, `static_assert_size`, `enum_from_u32`, `impl_tag`
- Tracing: `debug`, `trace`, `instrument`, `warn`
- Extensions: `extension` macro
- Collections: `smallvec`, `SmallVec` (explicit constructor)
- Others: `bitflags::bitflags!`, `scoped_thread_local!`

**Affected areas:**
- `rustc_ast/`, `rustc_borrowck/`, `rustc_codegen_*/`
- `rustc_middle/`, `rustc_hir/`, `rustc_infer/`
- `rustc_mir_*/`, `rustc_trait_selection/`
- `rustc_session/`, `rustc_target/`, `rustc_span/`
- ... and many more across the compiler

Trade-offs
----------
✅ **Better:** Explicit, clear, traceable imports  
⚠️ **Worse:** More verbose, more `use` statements at file tops