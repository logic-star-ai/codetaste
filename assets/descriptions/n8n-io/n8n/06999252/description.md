# Move WorkflowRepository to `@n8n/db` package

## Summary

Relocate `WorkflowRepository` from `packages/cli/src/databases/repositories/` to `packages/@n8n/db/src/repositories/` to consolidate database repositories in a centralized package.

## Why

- Follows established pattern—other repositories (`ExecutionRepository`, `SharedWorkflowRepository`, `CredentialsRepository`, etc.) already reside in `@n8n/db`
- Improves separation of concerns and code organization
- Makes repository accessible to other packages without circular dependencies
- Centralizes database layer logic

## Changes

**Repository relocation:**
- Move `workflow.repository.ts` from `packages/cli/src/databases/repositories/` → `packages/@n8n/db/src/repositories/`
- Export from `packages/@n8n/db/src/repositories/index.ts`

**Import updates:**
- Replace `@/databases/repositories/workflow.repository` → `@n8n/db` across ~80+ files
- Update internal imports within repository (e.g., `FolderRepository`, entities, utils)

**Type adjustments:**
- Move `ListQuery` type to `types-db`
- Adjust type imports accordingly

**Minor fixes:**
- Add `eslint-disable` comments for `any` types in query builder methods

## Scope

- Controllers (debug, workflows, public-api...)
- Services (execution, naming, hooks, active-workflows...)
- Commands (execute, export, import, list, update...)
- Tests (unit, integration...)
- Event relays, telemetry, webhooks, metrics...