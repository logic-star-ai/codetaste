# Refactor build operation types to use type token pattern

Reorganize rich build operation details/results types to decouple producer side (Gradle internals) from consumer side (build scan plugin) semantics using a type token pattern.