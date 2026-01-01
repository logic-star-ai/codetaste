# Refactor: Decouple `Command` from `KeyBindings` to support Mouse Bindings

## Summary

Refactor the Command and Key Bindings architecture to be generic, enabling Mouse Bindings to work alongside Key Bindings with a unified approach.

## Why

- `Command` was too tightly coupled with `KeyBindings`
- Commands needed to be invoked from mouse events (e.g., context menus)
- Architecture prevented building a `MouseBindings` equivalent
- Code duplication between different binding types

## Changes

**Core Architecture:**

- Made `CommandContext` generic → `CommandContext<TBinding>`
- Created `ICommandContext` interface
- Created `IInputBinding` interface  
- Added `InputBindings<TEvent, TBinding>` abstract base class

**KeyBindings Refactoring:**

- Removed `KeyBindingScope` enum entirely
- Split into three distinct binding collections:
  - `View.KeyBindings` - Focused bindings (only when View has focus)
  - `View.HotKeyBindings` - HotKey bindings (regardless of focus)
  - `Application.KeyBindings` - Application-scoped bindings
- `KeyBindings` now inherits from `InputBindings<Key, KeyBinding>`
- Simplified `KeyBinding` struct (removed `Scope`, added `Target`)

**Mouse Bindings Support:**

- Added `MouseBinding` struct implementing `IInputBinding`
- Added `MouseBindings` class inheriting from `InputBindings<MouseFlags, MouseBinding>`
- Added `View.MouseBindings` property
- Commands can now be bound to mouse events (e.g., `MouseBindings.Add(MouseFlags.Button3Clicked, Command.Context)`)

**API Changes:**

- `InvokeCommand` signature changed from `InvokeCommand(Command, Key?, KeyBinding?)` to `InvokeCommand<TBinding>(Command, TBinding)`
- Removed `KeyBindingScope` parameters throughout
- Updated method names (e.g., `GetKeyFromCommands` → `GetFirstFromCommands`)
- `CommandEventArgs.Context` now `ICommandContext?` instead of `CommandContext`

**Documentation:**

- Updated keyboard.md with Key Bindings architecture
- Added mouse.md for Mouse Bindings

## Breaking Changes

- `KeyBindingScope` removed
- `CommandContext` → `CommandContext<TBinding>`  
- Many API signatures changed
- `KeyBindings` API simplified (no more scope parameters)