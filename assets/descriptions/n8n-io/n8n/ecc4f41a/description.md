# Migrate UI tests from Cypress to Playwright

## Summary

Migrate UI end-to-end tests from Cypress to Playwright test framework. This migration includes creating a declarative test requirements system for improved test setup and maintainability.

## Why

- Modernize testing infrastructure
- Improve test isolation and consistency
- Enable more maintainable test setup through declarative configuration
- Better performance and reliability

## Tests Migrated

- ✅ `15-scheduler-node` - Schedule Trigger node execution
- ✅ `35-admin-user-smoke-test` - Admin user settings access
- ✅ `2270-ADO-opening-webhook-ndv-marks-workflow-as-unsaved` - Webhook node save state
- ✅ `46-n8n-io-iframe` - n8n.io iframe integration with telemetry
- ✅ `716-AI-bug-correctly-set-up-agent-model-shows-error` - AI Agent model error handling
- ✅ `9999-SUG-38-inline-expression-preview` - Expression preview in NDV
- ✅ `env-feature-flags` - Environment feature flags configuration
- 🔄 `45-ai-assistant` - AI Assistant (partial migration - 5 tests migrated, some remain)

## New Features Added

### TestRequirements System

Created declarative test setup system enabling:
- **Frontend Settings Override** - Merge custom settings with backend config
- **Feature Flags** - Enable/disable features declaratively
- **API Intercepts** - Mock API responses with flexible configuration
- **Workflow Imports** - Automatically import workflows for tests
- **Browser Storage** - Configure localStorage/sessionStorage

```typescript
const requirements: TestRequirements = {
  config: {
    features: { aiAssistant: true },
    settings: { telemetry: { enabled: false } }
  },
  workflow: { 'test_workflow.json': 'Test Workflow' },
  intercepts: {
    'ai-chat': {
      url: '**/rest/ai/chat',
      response: { sessionId: '1', messages: [...] }
    }
  },
  storage: { 'n8n-telemetry': '{"enabled": true}' }
};
```

### New Page Objects

- `AIAssistantPage` - AI Assistant interactions
- `BecomeCreatorCTAPage` - Creator CTA banner
- `IframePage` - Iframe element handling
- `SettingsPage` - Settings navigation
- `VersionsPage` - Version updates panel
- `WorkflowActivationModal` - Workflow activation dialog
- `WorkflowSettingsModal` - Workflow settings dialog

### Enhanced Existing Pages

- `CanvasPage` - Added production checklist methods, tags, zoom controls
- `NodeDisplayViewPage` - Added execute/output methods
- `WorkflowComposer` - Improved workflow import with unique naming

## Changes Made

### Infrastructure
- Context-aware settings intercepts (per-test isolation)
- Enhanced API helpers with feature flag methods
- Improved error handling and test fixtures

### Test Files
- Migrated Cypress tests marked as `.skip` with `// Migrated to Playwright` comments
- New Playwright test files in `packages/testing/playwright/tests/ui/`
- Added workflow fixtures for tests requiring pre-imported workflows

### Dependencies
- Added `@n8n/api-types` to testing package
- Added `nanoid` for unique test data generation

## Implementation Details

- All migrated tests use new `setupRequirements()` fixture for consistent setup
- Workflow imports now use unique IDs instead of timestamps for better test isolation
- API intercepts support flexible response configuration including network errors
- Settings override system properly merges with backend settings like Cypress behavior