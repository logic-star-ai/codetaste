# Refactor: Consolidate RBAC code into `@n8n/permissions` package with tests and documentation

RBAC code has leaked throughout the codebase instead of being properly abstracted in `@n8n/permissions`. This refactoring consolidates permission-related logic, adds comprehensive test coverage, and improves documentation.