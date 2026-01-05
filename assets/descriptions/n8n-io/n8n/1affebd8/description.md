# Refactor: Remove roleId indirection and simplify RBAC

## Summary
Replace role ID-based indirection with inline role strings. Convert `roleId` foreign keys in `user`, `shared_workflow`, and `shared_credentials` tables to `role` string columns storing values like `'global:owner'`, `'workflow:owner'`, `'credential:owner'`.

## Why
- Eliminate unnecessary DB joins for role lookups
- Simplify permission checks throughout codebase
- Reduce complexity by removing role mapping layer
- Prepare foundation for future RBAC improvements

## Changes

### Database Schema
- `user.globalRoleId` → `user.role` (e.g., `'global:owner'`)
- `shared_workflow.roleId` → `shared_workflow.role` (e.g., `'workflow:owner'`)  
- `shared_credentials.roleId` → `shared_credentials.role` (e.g., `'credential:owner'`)
- Migration `DropRoleMapping1705429061930` converts existing role IDs to strings

### Removed Components
- `RoleService` - no more role lookups
- `RoleRepository` - no more role table queries
- `RoleController` - `/roles` endpoint removed
- `Role` entity relations (table kept for potential future use)
- All `globalRoleId`/`roleId` foreign keys

### Type System
```typescript
type GlobalRole = 'global:owner' | 'global:admin' | 'global:member'
type WorkflowSharingRole = 'workflow:owner' | 'workflow:editor' | ...
type CredentialSharingRole = 'credential:owner' | 'credential:user'
```

### Authorization
- `authorize(['owner', 'admin'])` → `authorize(['global:owner', 'global:admin'])`
- `user.globalRole.name === 'owner'` → `user.role === 'global:owner'`
- `shared.role.name === 'owner'` → `shared.role === 'workflow:owner'`
- Direct string comparison instead of DB lookups

### Query Simplification
- No more `relations: ['globalRole']`, `relations: ['shared.role']`
- Direct role string filtering: `where: { role: 'workflow:owner' }`
- Eliminated role service injections across controllers/services

### Frontend
- Updated to use new role string format
- `user.globalRole?.name` → `user.role`