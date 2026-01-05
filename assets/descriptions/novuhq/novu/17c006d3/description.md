Title
-----
Remove `ApiException` in favor of `BadRequestException`

Summary
-------
Replace custom `ApiException` with standard NestJS `BadRequestException` across all services (`api`, `worker`, `ws`, `webhook`, `application-generic`).

Why
---
- `ApiException` is just an empty extension of `BadRequestException` with no added functionality
- Usage was inconsistent: ~60% `BadRequestException`, ~40% `ApiException` across codebase
- `ApiException` was duplicated/imported inconsistently from different locations
- Using NestJS standard `BadRequestException` directly is simpler and more idiomatic

Changes
-------
- Delete `ApiException` class definitions from `apps/.../shared/exceptions/api.exception.ts`
- Replace all `throw new ApiException(...)` → `throw new BadRequestException(...)`
- Update imports: remove `ApiException`, add `BadRequestException` from `@nestjs/common`

Affected Areas
--------------
- Auth (login, password reset, registration, switch org, ...)
- Events (trigger, parse, verify payload, ...)
- Workflows (create, update, delete, ...)
- Subscribers (update, channels, ...)
- Integrations (create, update, delete, webhook, ...)
- Notifications (get, mark, update, remove, ...)
- Partner integrations (Vercel)
- Templates (compile, create, delete, ...)
- Inbox, Widgets, Feeds, Layouts, ...

Impact
------
No breaking change - exception type/instance not exposed over HTTP/SDK.