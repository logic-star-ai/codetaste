# Title
Consolidate guards, decorators, and utilities into cohesive modules

# Summary
Refactor server code organization by consolidating auth-related components into `app.guard.ts`, moving domain utilities to `domain.util.ts`, and establishing clear boundaries between API and domain layers.

# Why
- Auth decorators, guards, and interfaces were scattered across multiple files
- Validation/transform utilities used in domain DTOs lived in `immich/` layer
- File fragmentation made code harder to navigate and maintain
- Unclear separation between API-specific and domain-level code

# Changes

**Consolidation**
- Merge all auth-related code into `app.guard.ts`:
  - `AuthGuard` → `AppGuard` 
  - Decorators: `Authenticated`, `PublicRoute`, `SharedLinkRoute`, `AdminRoute`, `AuthUser`, `GetLoginDetails`
  - Interfaces: `AuthRequest`, `AuthenticatedOptions`
  - Metadata enum

**Domain Migration**
- Move domain-level utilities to `domain/domain.util.ts`:
  - `ValidateUUID` decorator
  - Transform helpers: `toBoolean`, `toEmail`, `toSanitized`
- Export `AuthUserDto` from domain layer

**App-Level Utils**
- Move `UseValidation`, `patchFormData` to `app.utils.ts`

**Cleanup**
- Remove fragmented files:
  - `decorators/auth-user.decorator.ts`
  - `decorators/authenticated.decorator.ts`
  - `decorators/use-validation.decorator.ts`
  - `decorators/validate-uuid.decorator.ts`
  - `utils/transform.util.ts`
  - `utils/path-form-data.util.ts`
  - `middlewares/auth.guard.ts`

**Import Updates**
- Update ~40+ files to import from new locations