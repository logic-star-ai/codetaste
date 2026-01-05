# Title

Refactor `workflowHelpers` mixin to composable

# Summary

Convert the `workflowHelpers` mixin from Options API to Composition API using `useWorkflowHelpers()` composable.

# Changes

**Mixin → Composable Migration**
- Deleted `packages/editor-ui/src/mixins/workflowHelpers.ts`
- Created `packages/editor-ui/src/composables/useWorkflowHelpers.ts`
- Moved all workflow helper functions to the composable: `resolveParameter`, `getCurrentWorkflow`, `getConnectedNodes`, `saveCurrentWorkflow`, `saveAsNewWorkflow`, `getWorkflowDataToSave`, `checkReadyForExecution`, etc.

**Usage Pattern Updates**
- Removed `mixins: [workflowHelpers]` from components
- Added `setup()` hook with `const workflowHelpers = useWorkflowHelpers(router)`
- Updated method calls from `this.methodName()` to `this.workflowHelpers.methodName()` or `workflowHelpers.methodName()`

**Import Changes**
- All imports updated: `@/mixins/workflowHelpers` → `@/composables/useWorkflowHelpers`
- Updated in: components (Assignment, CodeNodeEditor, FilterConditions, ParameterInput, ResourceLocator, VariableSelector, WorkflowLMChat, etc.), views (NodeView, TemplatesView), mixins (expressionManager, pushConnection, workflowActivate, workflowRun), and tests

**API Changes**
- Composable now requires `router` parameter: `useWorkflowHelpers(router)`
- Uses `computed()` for reactive properties (e.g., `workflowPermissions`)
- Direct store access via `useXStore()` instead of `mapStores`

**Affected Components**
- ~40+ components updated across the codebase
- Key views: NodeView, ExecutionsList, DuplicateWorkflowDialog, WorkflowDetails, NodeDetailsView, TriggerPanel
- Expression/parameter components: ParameterInput, ResourceLocator, FilterConditions, AssignmentCollection
- Tests updated accordingly

# Why

- **Modern Vue 3 patterns**: Embrace Composition API for better code organization
- **Improved TypeScript support**: Better type inference and explicit dependencies
- **Enhanced testability**: Composables are easier to unit test than mixins
- **Clearer dependencies**: Explicit imports and parameters vs implicit mixin injection
- **Better code reusability**: Composables can be composed more flexibly than mixins