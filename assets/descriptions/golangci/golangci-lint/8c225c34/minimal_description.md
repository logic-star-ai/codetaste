# Simplify linter constructors with single-analyzer helper and fluent config API

Introduce `NewLinterFromAnalyzer()` constructor and `WithConfig()` method to reduce boilerplate in 90+ linter definitions that use a single analyzer.