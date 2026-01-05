# Refactor: Remove foreign crate re-exports from `zellij-utils`

## Summary

Remove re-exports of third-party crates from `zellij-utils` and make dependent crates declare these dependencies explicitly in their `Cargo.toml` files.

## Why

`zellij-utils` previously re-exported a bundle of foreign dependencies (`anyhow`, `nix`, `lazy_static`, `regex`, `vte`, `signal-hook`, `interprocess`, etc.) at the crate root. Other components used these re-exports via `zellij_utils::some_crate::...` instead of depending on the crates directly.

This caused problems:
- **Poor API clarity**: Hard to distinguish internal `zellij-utils` code from foreign re-exports
- **Hidden dependencies**: Dependants don't enumerate their actual dependencies, making it look like certain crates are only used in `zellij-utils` when they're actually used elsewhere
- **Maintenance overhead**: Difficult to track and manage dependencies across the codebase

## Changes

- Remove re-export block from `zellij-utils/src/lib.rs`
- Add explicit dependencies to:
  - `zellij-client/Cargo.toml`
  - `zellij-server/Cargo.toml`
  - `zellij-tile/Cargo.toml`
  - `zellij/Cargo.toml` (root)
- Promote commonly-used dependencies to workspace dependencies in root `Cargo.toml`
- Update imports throughout codebase: `zellij_utils::some_crate` → `some_crate`

## Result

Each component now explicitly declares its dependencies, making the dependency graph transparent and maintainable.