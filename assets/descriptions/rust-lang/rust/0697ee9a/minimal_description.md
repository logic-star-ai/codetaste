# Rename `ptr::from_exposed_addr` to `ptr::with_exposed_provenance`

Rename the pointer provenance API `ptr::from_exposed_addr` → `ptr::with_exposed_provenance` (and `_mut` variant) throughout the codebase, including compiler internals, documentation, and tests.