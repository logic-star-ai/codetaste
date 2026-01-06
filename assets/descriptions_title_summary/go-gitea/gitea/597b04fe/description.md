# Refactor: Remove `db.DefaultContext` usage across models and services (round 2)

Continue refactoring to eliminate `db.DefaultContext` usage by adding `context.Context` parameters to functions that previously relied on the global default context.