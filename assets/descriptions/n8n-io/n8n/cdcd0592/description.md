# Title
-----
Refactor: Consolidate RBAC code into `@n8n/permissions` package with tests and documentation

# Summary
-------
RBAC code has leaked throughout the codebase instead of being properly abstracted in `@n8n/permissions`. This refactoring consolidates permission-related logic, adds comprehensive test coverage, and improves documentation.

# Why
---
- Permission logic scattered across multiple packages (`@n8n/db`, `@n8n/api-types`, CLI)
- Duplicate role/scope definitions in various locations
- Inconsistent permission checking patterns
- Missing tests for permission logic
- Lack of documentation for RBAC utilities

# What Changed
---
**Package Restructuring**
- Moved `projectRoleSchema` from `@n8n/api-types` → `@n8n/permissions`
- Moved role types (`CredentialSharingRole`, `WorkflowSharingRole`, etc.) from `@n8n/db` → `@n8n/permissions`
- Removed user methods (`hasGlobalScope`, `globalScopes`, `isOwner`) from User entity

**Better Organization**
- Restructured into `/roles`, `/utilities`, `/schemas` directories
- Created `ALL_ROLES` map with role metadata (name, scopes, licensed status)
- Consolidated all role-to-scope mappings in `role-maps.ee.ts`
- Split scope definitions into dedicated files (`global-scopes.ee.ts`, `project-scopes.ee.ts`, ...)

**New Utilities**
- `hasGlobalScope()` - Check if auth principal has global scopes
- `getGlobalScopes()` - Get scopes for principal's role
- `getRoleScopes()` - Get scopes for any role, with optional resource filters
- `rolesWithScope()` - Find roles that have specific scope(s)

**Type Improvements**
- Added `AuthPrincipal` interface for authenticated entities
- Unified role type definitions with zod schemas
- Type-level tests to catch issues during typecheck

**Test Coverage**
- Tests for `combineScopes`, `hasScope`, `hasGlobalScope`, `rolesWithScope`
- Schema validation tests for all role types
- Type-level tests for `Scope` and `ApiKeyScope`

**Usage Updates**
- Replaced `user.hasGlobalScope()` → `hasGlobalScope(user, ...)`
- Replaced `roleService.getRoleScopes()` → `getRoleScopes()`
- Replaced `roleService.rolesWithScope()` → `rolesWithScope()`
- Updated repositories/services to use utilities from `@n8n/permissions`

**Documentation**
- Added JSDoc comments to all public utilities
- Documented parameters and return types
- Added usage examples