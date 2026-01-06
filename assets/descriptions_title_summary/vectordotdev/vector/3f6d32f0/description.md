# Migrate away from deprecated `chrono` functions to `_opt` variants

Replace deprecated `chrono` date/time construction functions with their non-panicking `_opt` counterparts throughout the codebase in preparation for upgrading the `chrono` dependency.