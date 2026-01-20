# Refactor: Move `mir::Field` to `abi::FieldIdx`

Move the `Field` type from `rustc_middle::mir` to `rustc_abi` and rename it to `FieldIdx`. Update all imports and usages throughout the codebase accordingly.