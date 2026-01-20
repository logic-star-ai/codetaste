# Rename `rustc_abi::Abi` to `BackendRepr`

Rename `rustc_abi::Abi` enum to `BackendRepr` and rename the `Aggregate` variant to `Memory`. This addresses long-standing confusion between backend representation and actual calling conventions.