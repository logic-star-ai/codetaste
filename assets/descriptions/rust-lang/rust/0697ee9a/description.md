Title
-----
Rename `ptr::from_exposed_addr` to `ptr::with_exposed_provenance`

Summary
-------
Rename the pointer provenance API `ptr::from_exposed_addr` → `ptr::with_exposed_provenance` (and `_mut` variant) throughout the codebase, including compiler internals, documentation, and tests.

Why
---
The old name `from_exposed_addr` is misleading—it's the **provenance** being exposed, not the address. The function signature takes an address and returns a pointer **with** exposed provenance. The new name:
- More accurately describes the operation
- Better matches the existing `ptr::without_provenance` API
- Improves API consistency

(`ptr::expose_addr()` remains unchanged, as no better alternative found yet. Intended meaning: "expose the provenance and return the address")

Changes Required
----------------
**Core library APIs:**
- `ptr::from_exposed_addr` → `ptr::with_exposed_provenance`
- `ptr::from_exposed_addr_mut` → `ptr::with_exposed_provenance_mut`
- Portable SIMD: `SimdConstPtr::from_exposed_addr` → `with_exposed_provenance`
- Portable SIMD: `SimdMutPtr::from_exposed_addr` → `with_exposed_provenance`

**Compiler internals:**
- MIR: `CastKind::PointerFromExposedAddress` → `CastKind::PointerWithExposedProvenance`
- Intrinsic: `simd_from_exposed_addr` → `simd_with_exposed_provenance`
- Symbol: Update `rustc_span::symbol`
- Update all compiler passes (borrowck, codegen, const_eval, validation, ...)

**Documentation & diagnostics:**
- Update error messages in `hir_typeck/messages.ftl`
- Update `FUZZY_PROVENANCE_CASTS` lint docs
- Update Miri documentation and diagnostics
- Update doc comments throughout

**Tests:**
- Update test expectations (`.stderr` files)
- Update test code using the old API

**Bootstrap compatibility:**
- Use `#[cfg(bootstrap)]` for staged rollout