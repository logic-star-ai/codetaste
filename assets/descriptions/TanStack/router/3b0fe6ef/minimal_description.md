# Refactor(router-core): Extract framework-agnostic logic into separate package

Extract shared router logic from `react-router` into new `@tanstack/router-core` package. Maintain backwards compatibility via re-exports.