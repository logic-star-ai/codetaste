# Refactor: Remove foreign crate re-exports from `zellij-utils`

Remove re-exports of third-party crates from `zellij-utils` and make dependent crates declare these dependencies explicitly in their `Cargo.toml` files.