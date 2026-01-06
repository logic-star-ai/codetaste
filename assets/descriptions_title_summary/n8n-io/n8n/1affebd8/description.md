# Refactor: Remove roleId indirection and simplify RBAC

Replace role ID-based indirection with inline role strings. Convert `roleId` foreign keys in `user`, `shared_workflow`, and `shared_credentials` tables to `role` string columns storing values like `'global:owner'`, `'workflow:owner'`, `'credential:owner'`.