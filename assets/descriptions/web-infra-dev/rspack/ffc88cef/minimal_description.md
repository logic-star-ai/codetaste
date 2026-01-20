# Refactor: Module build methods to directly update `build_info` and `build_meta`, remove `Option` wrappers

Simplify module build API by having `Module::build()` directly update internal `build_info` and `build_meta` fields instead of returning them, and remove `Option` wrappers from trait methods.