# Refactor: Remove lifetime annotations from `Rpc` type

## Summary
Remove the lifetime parameter from the `Rpc` type, transitioning from `Rpc<'a>` to `Rpc`. Make the type self-contained by owning its data instead of holding references.

## Changes

### Core Type Simplification
- Remove lifetime parameter `'a` from `Rpc<'a>` → `Rpc`
- Change `ctx: &'a Context` → `ctx: Context` (owned)
- Change `opts: &'a CommandGlobalOpts` → `opts: CommandGlobalOpts` (owned)
- Add `#[derive(AsyncTryClone)]` for async cloning support

### `RpcMode` Refactoring
- Remove `RpcBuilder` (no longer needed)
- Simplify `RpcMode::Background { tcp: Option<&'a TcpTransport> }` → `RpcMode::Background(Arc<TcpTransport>)`
- Always create TCP transport, wrap in `Arc` for shared ownership

### API Changes
- Make `Rpc::background()` async (now creates TCP transport)
- Update all function signatures: `&mut Rpc<'a>` → `&mut Rpc`
- Replace `.clone()` with `.async_try_clone().await` where needed
- Add `set_to()` method for updating route

### Benefits
- Eliminates lifetime complexity across the codebase
- Enables passing `&mut Rpc` instead of recreating from `Context + CommandGlobalOpts`
- Simplifies async cloning semantics
- Reduces cognitive overhead for maintainers

## Files Modified
- `util/mod.rs` - Core `Rpc` type changes
- `*.rs` - Update call sites throughout (100+ locations)