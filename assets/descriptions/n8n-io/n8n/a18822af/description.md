# Refactor: Extract API Request Logic into `@n8n/rest-api-client` Package

## Summary
Extract API request-related code from `editor-ui` into a new standalone package `@n8n/rest-api-client` to improve code organization and reusability.

## Why
- API request logic was tightly coupled with `editor-ui`
- Improve separation of concerns
- Enable potential reuse of API client in other frontend packages
- Better package structure for scalability

## Changes

### New Package Structure
Create `packages/frontend/@n8n/rest-api-client/` with:
- API modules: `api-keys`, `communityNodes`, `ctas`, `eventbus`, `events`, `mfa`, `nodeTypes`, `npsSurvey`, `orchestration`, `roles`, `ui`, `webhooks`
- Core utilities: `utils.ts` (formerly `apiUtils.ts`)
- Types: `IRestApiContext` interface
- Tests: `utils.test.ts`

### File Migrations
Move from `editor-ui/src/api/`:
- `api-keys.ts` → `@n8n/rest-api-client/src/api/api-keys.ts`
- `communityNodes.ts` → `@n8n/rest-api-client/src/api/communityNodes.ts`
- `ctas.ts` → `@n8n/rest-api-client/src/api/ctas.ts`
- `eventbus.ee.ts` → `@n8n/rest-api-client/src/api/eventbus.ee.ts`
- `events.ts` → `@n8n/rest-api-client/src/api/events.ts`
- `mfa.ts` → `@n8n/rest-api-client/src/api/mfa.ts`
- `nodeTypes.ts` → `@n8n/rest-api-client/src/api/nodeTypes.ts`
- `npsSurvey.ts` → `@n8n/rest-api-client/src/api/npsSurvey.ts`
- `orchestration.ts` → `@n8n/rest-api-client/src/api/orchestration.ts`
- `roles.api.ts` → `@n8n/rest-api-client/src/api/roles.ts`
- `ui.ts` → `@n8n/rest-api-client/src/api/ui.ts`
- `webhooks.ts` → `@n8n/rest-api-client/src/api/webhooks.ts`

Move from `editor-ui/src/utils/`:
- `apiUtils.ts` + `apiUtils.test.ts` → `utils.ts` + `utils.test.ts`

### Constant Extraction
- Extract `BROWSER_ID_STORAGE_KEY` → `@n8n/constants/src/browser.ts`

### Utility Refactoring
- Move `unflattenExecutionData` from `apiUtils` → `executionUtils.ts` (stays in `editor-ui`)

### Update Imports
Update all references across `editor-ui` and other packages to import from `@n8n/rest-api-client`

### Configuration Updates
- Add package to workspace
- Configure build tooling (tsup, vite, vitest)
- Update path mappings in tsconfig
- Enhance `@n8n/vitest-config` with `createVitestConfig()` factory