# Refactor Environment Setup: WebGLProbe, Dispose Method, and Helper Functions

## Summary

Refactor environment handling to improve separation between browser and node environments, add `WebGLProbe` to env, replace `isLikelyNode` flag with test-specific helpers, and introduce env-specific disposal method.

## Changes

### WebGL/GL Probe Architecture
- Abstract `GLProbe` base class introduced
- `WebGLProbe` (browser) and `NodeGLProbe` (node stub) implementations
- Moved to `env.WebGLProbe` property
- Renamed `WebGLPrecision` → `GLPrecision`
- Removed global `webGLProbe` instance

### Environment Cleanup
- Removed `cleanUpJsdomNode()` utility function
- Added `env.dispose(element)` method:
  - Browser: noop
  - Node: cleans up JSDOM implementation details (`_image`, `_canvas`, etc.)
- Updated all canvas disposal code to use `getEnv().dispose()`

### Environment Access Pattern
- Added `getWindow()` and `getDocument()` helper functions
- Replaced `getEnv().window` → `getWindow()` throughout codebase
- Replaced `getEnv().document` → `getDocument()` throughout codebase
- Improved type safety (supports `Window | DOMWindow`)

### Node Environment
- Removed `isLikelyNode` flag from env
- Tests use `isNode()` function (defined in test config)
- Moved `getNodeCanvas()` to node env file
- Improved JSDOM configuration (`pretendToBeVisual: true`, etc.)
- Removed `setEnvForTests` wrapper

### Other
- Removed `requestAnimationFrame` polyfill (use native implementation)
- Cleaned up rollup externals
- Updated build workflow checkout paths

## Why

- **Better architecture**: GL probing is environment-specific and belongs in env
- **Cleaner API**: `env.dispose()` is more explicit than utility function
- **Type safety**: Helper functions provide better types
- **Maintainability**: Easier to find/replace window/document access
- **Separation of concerns**: Environment details properly encapsulated