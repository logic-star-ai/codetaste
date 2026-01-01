# Split database-dependent types from `interfaces.ts` into `types-db.ts`

## Summary
Extract all types in `packages/cli/src/interfaces.ts` that depend (directly or transitively) on database entities into a new file `packages/cli/src/types-db.ts`. Fold `workflows.types.ts` into `types-db.ts` as well.

## Why
Preparing to move database entities to `@n8n/db` package for consumption by both `cli` and `@n8n/sdk`. Since entities are heavily interrelated with types in `interfaces.ts`, the entity-dependent types need to be separated so they can move together with entities in a future refactor.

## Types to Extract
Move to `types-db.ts`:
- `IWorkflowDb`
- `ICredentialsDb` / `ICredentialsBase`
- `IExecutionBase` / `IExecutionResponse`
- `PublicUser`
- `IPersonalizationSurveyAnswers`
- `ITagDb` / `ITagWithCountDb` / `ITagBase`
- `IAnnotationTagDb` / `IAnnotationTagWithCountDb`
- `UserSettings`
- `SlimProject`
- `UsageCount`
- All types from `workflows.types.ts`:
  - `WorkflowWithSharingsAndCredentials`
  - `WorkflowWithSharingsMetaDataAndCredentials`
  - `CredentialUsedByWorkflow`

## Changes Required
- [ ] Create `packages/cli/src/types-db.ts`
- [ ] Move entity-dependent types from `interfaces.ts` → `types-db.ts`
- [ ] Fold `workflows/workflows.types.ts` → `types-db.ts`
- [ ] Delete `workflows/workflows.types.ts`
- [ ] Update imports across codebase:
  - Controllers (`me.controller.ts`, `auth.controller.ts`, `users.controller.ts`, ...)
  - Services (`user.service.ts`, `tag.service.ts`, `annotation-tag.service.ee.ts`, ...)
  - Repositories (`execution.repository.ts`, `tag.repository.ts`, ...)
  - Commands, migrations, tests, webhooks, events, ...
  - Change `from '@/interfaces'` → `from '@/types-db'` where appropriate

## Result
Clean separation between:
- `interfaces.ts` - types independent of DB entities
- `types-db.ts` - types dependent on DB entities (ready to move with entities later)