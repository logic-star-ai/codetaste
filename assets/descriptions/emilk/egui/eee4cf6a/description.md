# Replace Context lock guards with closure-based API to prevent deadlocks

## Summary
Refactor `Context` (and `Ui`) accessor methods to use closures instead of returning `RwLockReadGuard`/`RwLockWriteGuard`. This prevents accidental double-locking deadlocks.

## Why
Previously easy to deadlock:
```rust
if let Some(pos) = ctx.input().pointer.latest_pos() {
    // ctx is still locked here - any ctx call deadlocks!
}
```

Now safe:
```rust
if let Some(pos) = ctx.input(|i| i.pointer.latest_pos()) {
    // ctx lock released - safe to use ctx here
}
```

## Changes

### API Changes (Breaking)
- `ctx.input()` → `ctx.input(|i| ...)`
- `ctx.memory()` → `ctx.memory(|mem| ...)`  
- `ctx.memory_mut()` → `ctx.memory_mut(|mem| ...)`
- `ctx.output()` → `ctx.output(|o| ...)`
- `ctx.data()` → `ctx.data(|d| ...)`
- `ctx.fonts()` → `ctx.fonts(|f| ...)`
- `ctx.options()` → `ctx.options(|o| ...)`
- `ui.input()`, `ui.memory()`, ... same pattern

### Internal Refactoring
- `Context::read()` / `write()` now take closures
- `frame_state()`, `graphics_mut()`, etc. use closure pattern
- Remove `ShortRwLockHelper`

### New Helpers
- `ctx.screen_rect()` - shorthand for `ctx.input(|i| i.screen_rect())`
- `ctx.set_cursor_icon()` - shorthand for `ctx.output_mut(|o| o.cursor_icon = ...)`

### Documentation
- Updated `Context` docs explaining locking model
- Added examples showing proper usage
- Migration guide in CHANGELOG

## Migration
Replace all `.input()`, `.memory()`, etc. calls with closure-based versions:
```rust
// Before
let pressed = ctx.input().key_pressed(Key::A);

// After  
let pressed = ctx.input(|i| i.key_pressed(Key::A));
```