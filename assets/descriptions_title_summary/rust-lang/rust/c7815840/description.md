# Extract `fluent_messages!` macro into separate `rustc_fluent_macro` crate

Move the `fluent_messages!` macro from `rustc_macros` into a new dedicated crate `rustc_fluent_macro` to decouple fluent/icu4x dependencies from the core macro infrastructure.