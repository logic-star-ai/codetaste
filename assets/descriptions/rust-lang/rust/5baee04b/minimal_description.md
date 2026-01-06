# Remove `#[macro_use] extern crate tracing` from multiple compiler crates

Replace implicit macro imports via `#[macro_use] extern crate tracing` with explicit `use` statements for tracing macros across compiler crates.