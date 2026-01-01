# Title
Rename `SessionContext::with_*` constructors to `SessionContext::new_with_*` for consistency with Rust idioms

# Summary
Rename constructor methods in `SessionContext` and `SessionState` that currently start with `with_` to instead start with `new_with_` to follow Rust naming conventions where `with_` methods modify existing instances while `new_` methods create new ones.

# Why
Current naming is inconsistent and confusing:
- Methods like `SessionContext::with_config_rt()` **create** new instances
- In DataFusion, most `with_*` methods **update** existing fields
- This violates Rust idioms where `new_*` indicates construction

# Changes
Rename the following methods:
- `SessionContext::with_config` → `SessionContext::new_with_config`
- `SessionContext::with_config_rt` → `SessionContext::new_with_config_rt`
- `SessionContext::with_state` → `SessionContext::new_with_state`
- `SessionState::with_config_rt` → `SessionState::new_with_config_rt`
- `SessionState::with_config_rt_and_catalog_list` → `SessionState::new_with_config_rt_and_catalog_list`

Add deprecation warnings to old names pointing to new ones.

Remove `default_session_builder` (deprecated ~10 releases ago).

# Migration
Old methods remain with deprecation warnings, allowing gradual migration:
```rust
// Old (deprecated)
SessionContext::with_config(config)

// New
SessionContext::new_with_config(config)
```