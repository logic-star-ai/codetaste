# Remove `enableOwnerStacks` Feature Flag

## Summary

Remove the `enableOwnerStacks` feature flag and associated conditional logic throughout the codebase. The owner stacks feature has landed everywhere and is now permanently enabled.

## Why

- Feature has been fully rolled out and stabilized
- No longer need to maintain dual code paths
- Simplifies codebase by removing ~2000+ lines of conditional logic
- Reduces test complexity and maintenance burden

## Changes Required

### Feature Flag Files
- Remove `enableOwnerStacks` declaration from:
  - `ReactFeatureFlags.js`
  - `ReactFeatureFlags.*.js` (all forks: native-fb, native-oss, test-renderer, www, etc.)

### Core Implementation
- Remove `enableOwnerStacks` checks in:
  - `ReactFlightClient.js` - simplify element creation, stack handling, component info
  - `ReactFlightServer.js` - remove conditional stack/task initialization  
  - `ReactFizzServer.js` - consolidate debug stack/task handling
  - `ReactJSXElement.js` - always include `_debugStack` and `_debugTask` properties
  - `consoleMock.js` - remove fallback getCurrentStack logic
  - `ReactOwnerStack.js` - always use owner stack approach
  - `ReactComponentInfoStack.js` - remove guard checks
  - `ReactComponentStackFrame.js` - delete unused `describeUnknownElementTypeFrameInDEV`
  - `DOMPluginEventSystem.js` - remove conditional owner stack captures
  - Various DOM/event handling files

### Test Updates
- Remove `gate(flags => flags.enableOwnerStacks)` conditionals from ~50+ test files
- Consolidate dual test expectations into single expected behavior
- Remove alternate assertion branches
- Update inline snapshots to reflect single code path
- Clean up `@gate` decorators that check flag

### Specific Cleanup Areas
- **JSX validation**: Always validate with owner stacks, remove legacy key warning logic
- **Error messages**: Consolidate to owner stack format
- **Component stacks**: Always use owner-based approach  
- **Console assertions**: Single expectation path in test utilities
- **Debug properties**: Always attach `_debugStack`/`_debugTask` to elements

## Files Affected (Major)

- `packages/react/src/jsx/ReactJSXElement.js`
- `packages/react-client/src/ReactFlightClient.js`
- `packages/react-server/src/ReactFlightServer.js`
- `packages/react-server/src/ReactFizzServer.js`
- `packages/internal-test-utils/consoleMock.js`
- `packages/shared/ReactFeatureFlags.js`
- ~60+ test files with conditional assertions

## Testing

All existing tests should pass with flag removed since owner stacks is now the default behavior everywhere.