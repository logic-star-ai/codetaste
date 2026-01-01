# Title

Simplify WASI internal implementations by removing generic wrapper types

# Summary

Refactor WASIp2 implementation to remove generic wrapper types (`WasiImpl<T>`, `IoImpl<T>`, `WasiHttpImpl<T>`) and implement Host traits directly for concrete view types instead.

# Why

Current implementation uses complex generic wrappers:
- `impl<T> Host for WasiImpl<T> where T: WasiView` 
- Extra layer of indirection making code baroque and non-obvious
- Forces everything generic → minimal code in `wasmtime-wasi` crate → longer codegen times for consumers
- `WasiView` inherits from `IoView` creating tight coupling
- Requires forwarding impls like `impl<T: WasiView> WasiView for &mut T`
- Blocks WASIp3 work requiring simultaneous table/ctx borrow

# Changes

**Trait hierarchy:**
- Decouple `WasiView` from `IoView` - now unrelated traits
- `WasiView::ctx()` now returns `WasiCtxView<'a>` containing both `ctx: &'a mut WasiCtx` and `table: &'a mut ResourceTable`

**Implementation targets:**
- Host traits now `impl Host for WasiCtxView<'_>` (no generics)
- `wasi:io` traits now `impl Host for ResourceTable` (no `IoImpl<T>`)
- Remove all `*Impl<T>` wrapper types

**Embedder changes:**
- No longer implement `IoView` directly - fold into `WasiView`
- `WasiHttpView` gets direct `fn table()` method instead of inheriting `IoView`

# Benefits

- Easier to understand - no generic wrapper indirection
- Better compile times - concrete impls generate code in `wasmtime-wasi` crate
- More modular - `wasi:clocks` doesn't need filesystem context
- Enables WASIp3 - simultaneous borrow of table/ctx now possible
- Aligns with WASIp3 prototype implementation style