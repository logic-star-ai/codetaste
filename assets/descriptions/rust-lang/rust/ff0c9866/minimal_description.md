# Remove `#[macro_use] extern crate tracing` from rustc crates (round 4)

Replace implicit macro importing via `#[macro_use] extern crate tracing` with explicit `use` statements across `rustc_*` crates.