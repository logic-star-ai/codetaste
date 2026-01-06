# Remove `#[macro_use] extern crate` declarations for explicit imports

Replace implicit macro imports via `#[macro_use] extern crate foo` with explicit `use` statements throughout the compiler codebase. This makes the code more verbose but significantly improves readability by making it clear where macros and types are defined.