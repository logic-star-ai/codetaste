# Migrate `Handle::weak_from_u128` to `weak_handle!` macro

Replace all uses of `Handle::weak_from_u128` with the new `weak_handle!` macro introduced in #17384. Deprecate `Handle::weak_from_u128` as it's no longer needed.