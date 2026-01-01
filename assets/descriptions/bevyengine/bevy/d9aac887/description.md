# Rename `Input` to `ButtonInput`

## Summary
Renamed `Input<T>` struct to `ButtonInput<T>` throughout the codebase to better reflect its purpose as a pressable button state tracker.

## Why
The generic name `Input` was misleading since:
- `bevy_input` contains multiple input types (buttons, axes, etc.)
- `Input<T>` specifically tracks pressable button states (pressed/just_pressed/just_released)
- Axis inputs and other input types don't fit this pattern
- Users unfamiliar with the docs were confused by the overly broad name

## Changes
- Renamed `crates/bevy_input/src/input.rs` → `button_input.rs`
- Changed struct name: `Input<T>` → `ButtonInput<T>`
- Updated all references across:
  - Core input systems (keyboard, mouse, gamepad)
  - Documentation and doc comments
  - Examples (2d, 3d, audio, games, tools, ui, window, etc.)
  - Tests
- Updated common conditions module
- Updated resource registrations in `InputPlugin`

## Migration Required
**Breaking Change**: Users must rename `Input` to `ButtonInput` in their projects.

```rust
// Before
fn system(input: Res<Input<KeyCode>>) { ... }

// After  
fn system(input: Res<ButtonInput<KeyCode>>) { ... }
```

Affects: `Input<KeyCode>`, `Input<MouseButton>`, `Input<GamepadButton>`, `Input<ScanCode>`