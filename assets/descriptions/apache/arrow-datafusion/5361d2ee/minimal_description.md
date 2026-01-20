# Rename `SessionContext::with_*` constructors to `SessionContext::new_with_*` for consistency with Rust idioms

Rename constructor methods in `SessionContext` and `SessionState` that currently start with `with_` to instead start with `new_with_` to follow Rust naming conventions where `with_` methods modify existing instances while `new_` methods create new ones.