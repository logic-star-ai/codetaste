# Refactor: Move `templates` API to `@n8n/rest-api-client` package

## Summary
Move templates API methods and related types from `editor-ui/src/api/templates.ts` to the `@n8n/rest-api-client` package for better code organization and separation of concerns.

## Why
- Consolidate API client code in dedicated package
- Improve code reusability across frontend packages
- Better separation between API layer and UI layer
- Consistent location for REST API interfaces and methods

## Changes

### New files in `@n8n/rest-api-client/src/api/`:
- **`templates.ts`** - All template API methods:
  - `testHealthEndpoint()`
  - `getCategories()`
  - `getCollections()`
  - `getWorkflows()`
  - `getCollectionById()`
  - `getTemplateById()`
  - `getWorkflowTemplate()`
- **`tags.ts`** - `ITag` interface
- **`workflows.ts`** - Workflow-related types:
  - `WorkflowData`, `WorkflowDataCreate`, `WorkflowDataUpdate`
  - `WorkflowMetadata`

### Type migrations from `Interface.ts`:
- Template types → `@n8n/rest-api-client/api/templates`:
  - `IWorkflowTemplate`, `IWorkflowTemplateNode`, `IWorkflowTemplateNodeCredentials`
  - `ITemplatesNode`, `ITemplatesCollection`, `ITemplatesCollectionFull`, `ITemplatesCollectionResponse`
  - `ITemplatesWorkflow`, `ITemplatesWorkflowFull`, `ITemplatesWorkflowResponse`, `ITemplatesWorkflowInfo`
  - `ITemplatesCategory`, `ITemplatesQuery`, `TemplateSearchFacet`
- `ITag` → `@n8n/rest-api-client/api/tags`
- Workflow types → `@n8n/rest-api-client/api/workflows`:
  - `IWorkflowData` → `WorkflowData`
  - `IWorkflowDataCreate` → `WorkflowDataCreate`
  - `IWorkflowDataUpdate` → `WorkflowDataUpdate`

### Deleted:
- `packages/frontend/editor-ui/src/api/templates.ts`
- Type definitions from `Interface.ts`
- Template state types from `Interface.ts` → moved to `templates.store.ts`

### Updated:
- ~80+ files with import path changes
- Export index in `@n8n/rest-api-client`
- `.prettierignore` - exclude auto-generated `components.d.ts`

## Testing
- ✅ No functional changes
- ✅ Type-only refactoring
- ✅ All imports updated consistently