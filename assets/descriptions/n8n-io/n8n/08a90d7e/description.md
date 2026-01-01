# Title
-----
Refactor: Migrate user-management routes to decorator-based controllers

# Summary
-------
Switch user-management routes from function-based handlers to decorator-based controller classes for better structure, maintainability, and testability.

# Why
---
- Current function-based route handlers (`authenticationMethods`, `meNamespace`, `usersNamespace`, ...) are less maintainable
- Decorator-based approach provides cleaner separation of concerns
- Constructor-based dependency injection improves testability
- Aligns with modern Node.js framework patterns (NestJS-style)

# Changes
---------
**Route Handlers → Controllers:**
- `UserManagement/routes/auth.ts` → `controllers/auth.controller.ts`
- `UserManagement/routes/me.ts` → `controllers/me.controller.ts`
- `UserManagement/routes/owner.ts` → `controllers/owner.controller.ts`
- `UserManagement/routes/passwordReset.ts` → `controllers/passwordReset.controller.ts`
- `UserManagement/routes/users.ts` → `controllers/users.controller.ts`

**New Decorator System:**
- `@RestController(basePath?)` - class decorator for base path
- `@Get(path)`, `@Post(path)`, `@Patch(path)`, `@Delete(path)` - method decorators for routes
- `registerController()` - registers decorated controllers with Express app

**Structure Changes:**
- `UserManagement/auth/jwt.ts` → `auth/jwt.ts`
- `UserManagement/middlewares/` → `middlewares/`
- Controllers receive dependencies via constructor (repositories, config, logger, hooks, ...)
- Centralized auth middleware setup in `setupAuthMiddlewares()`

**Registration:**
```typescript
// Old: Function-based
authenticationMethods.apply(this);
meNamespace.apply(this);

// New: Decorator-based
registerController(app, config, new AuthController({ ... }));
registerController(app, config, new MeController({ ... }));
```

# Notes
------
- No changes to business logic, purely structural
- Import paths updated throughout codebase (`@/UserManagement/...` → `@/controllers/...`)
- Test utilities updated to support new controller registration
- All user-management endpoints migrated in single commit