# Refactor: Consolidate FUZZ_TARGET macros into single variadic macro

Flatten the multiple `FUZZ_TARGET*` macro variants into a single `FUZZ_TARGET` macro that accepts options via designated initializers.