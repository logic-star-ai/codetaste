# Refactor: Reorganize error hierarchy in `core` and `workflow` packages

Reorganize error hierarchies in `core` and `workflow` packages to ensure all errors inherit from `ApplicationError` for normalized Sentry error reporting.