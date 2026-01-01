# Move `UserRepository` and subscribers to `@n8n/db`

## Summary
Relocate `UserRepository` and database subscribers from `cli` package to `@n8n/db` shared package to enable consumption by both `cli` and `@n8n/sdk`.

## Why
As part of the extensions project, these database components need to be accessible across multiple packages. Currently they're siloed in `cli`, preventing reuse in `@n8n/sdk`.

## What
- Move `packages/cli/src/databases/repositories/user.repository.ts` → `packages/@n8n/db/src/repositories/user.repository.ts`
- Move `packages/cli/src/databases/subscribers/*` → `packages/@n8n/db/src/subscribers/*`
- Export from `@n8n/db` index
- Update all imports across codebase:
  - Replace `@/databases/repositories/user.repository` → `@n8n/db`
  - Update ~40+ files importing `UserRepository`
  - Update subscriber references

## Changes
Files affected include:
- Controllers: `auth.controller.ts`, `me.controller.ts`, `users.controller.ts`, `invitation.controller.ts`, `owner.controller.ts`, `password-reset.controller.ts`, ...
- Services: `auth.service.ts`, `user.service.ts`, `access.service.ts`, `hooks.service.ts`, `ownership.service.ts`, ...
- Commands: `import/workflow.ts`, `ldap/reset.ts`, `user-management/reset.ts`, `community-node.ts`, ...
- LDAP/SAML: `ldap.ee/helpers.ee.ts`, `sso.ee/saml/*`, ...
- Tests: All integration tests importing `UserRepository`