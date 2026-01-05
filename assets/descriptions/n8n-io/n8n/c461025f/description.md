# Migrate externalHooks mixin to composables

## Summary
Migrate all `externalHooks` mixin usage to `useExternalHooks()` composable across the codebase as part of the NodeView refactor effort.

## Why
- Move from Vue 2 mixins pattern to Vue 3 Composition API
- Better code organization and maintainability
- Align with modern Vue 3 patterns
- Part of larger NodeView refactoring initiative

## Changes
- Remove `externalHooks` mixin from all components
- Replace `this.$externalHooks().run(...)` calls with `useExternalHooks().run(...)`
- Move `runExternalHook` from `@/utils/externalHooks` → `@/composables/useExternalHooks`
- Move `extendExternalHooks` from `@/mixins/externalHooks` → `@/hooks/register.ts`
- Delete `src/mixins/externalHooks.ts`
- Remove `IExternalHooks` interface from `Interface.ts`

## Affected Components
- App.vue
- CredentialEdit, CredentialsSelectModal
- ExecutionsList, ExecutionsView/ExecutionsList
- ExpressionEdit
- MainHeader, MainSidebar
- Node, NodeCreator/*, NodeDetailsView, NodeExecuteButton, NodeSettings*
- ParameterInput, PersonalizationModal
- RunData*, Sticky
- WorkflowActivator, WorkflowLMChat, WorkflowSettings
- NodeView, TemplatesCollectionView, TemplatesWorkflowView
- ...

## Testing
Run with `export N8N_DEPLOYMENT_TYPE=cloud` and verify hooks still execute as expected.