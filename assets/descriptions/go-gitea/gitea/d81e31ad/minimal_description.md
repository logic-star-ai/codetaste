# Refactor: Move db.Engine parameter to context.Context across codebase

Refactor almost all database access functions to accept `context.Context` instead of `db.Engine` as their first parameter, enabling better request scoping, cancellation support, and more idiomatic Go patterns.