# Refactor: Rename `util::config` module to `util::context`

## Summary

Rename the `util::config` module to `util::context` throughout the codebase to better reflect its purpose as the global application context container (which includes configuration parsing).

## Why

The module was named `config` but actually contains the `GlobalContext` structure and related functionality. The name `context` more accurately represents that this is the global application context, not just configuration.

This is a continuation of previous refactoring efforts in #13409 and #13486.

## Changes

- Move `src/cargo/util/config/*` → `src/cargo/util/context/*`
  - `de.rs`, `environment.rs`, `key.rs`, `mod.rs`, `path.rs`, `target.rs`, `value.rs`
- Update all imports: `use crate::util::config::*` → `use crate::util::context::*`
- Update all imports: `use cargo::util::config::*` → `use cargo::util::context::*`
- Rename function: `config_configure()` → `configure_gctx()`
- Update documentation references to reflect new module path
- Update triagebot configuration file paths

## Scope

Files affected:
- `src/cargo/util/{config → context}/*`
- `src/bin/cargo/cli.rs`
- `src/cargo/core/**/*.rs`
- `src/cargo/ops/**/*.rs`
- `src/cargo/sources/**/*.rs`
- `tests/testsuite/*.rs`
- `crates/xtask-bump-check/src/main.rs`
- `triagebot.toml`
- ... (various other files with imports)