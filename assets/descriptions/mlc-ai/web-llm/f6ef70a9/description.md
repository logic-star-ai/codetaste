# Refactor ChatModule to Engine

## Summary
Rename `ChatModule` to `Engine` throughout codebase to better reflect expanded functionality beyond simple chat. The name "ChatModule" is too narrow as the library now supports various modalities and use cases.

## Changes

### Core API
- Rename `ChatModule` → `Engine`
- Rename `ChatInterface` → `EngineInterface`
- Remove deprecated `ChatRestModule`
- Deprecate `generate()` in favor of OpenAI-style API

### Factory Methods
- Introduce `CreateEngine(modelId, engineConfig?)` for convenient initialization
- Introduce `CreateWebWorkerEngine(worker, modelId, engineConfig?)` for web worker setup
- Add `EngineConfig` type to wrap optional configurations (chatOpts, appConfig, initProgressCallback, logitProcessorRegistry)

### OpenAI API
- Add `engine.chat.completions.create()` as primary interface
- Finalize OpenAI-compatible API with streaming, json-mode, function-calling, seeding
- Expose APIs through `engine.chat.*` namespace

### Worker Support
- Rename `ChatWorkerHandler` → `EngineWorkerHandler`
- Rename `ChatWorkerClient` → `WebWorkerEngine`

### Examples
- Update all examples to use new `Engine` API
- Reorganize examples by category (basic chat, OpenAI capabilities, chrome extension, etc.)
- Separate OpenAI feature demos (streaming, json-mode, function-calling, seed-to-reproduce)
- Update README with new API usage patterns

## Migration
```typescript
// Before
const chat = new ChatModule();
await chat.reload(modelId);

// After
const engine = await CreateEngine(modelId);
// or
const engine = new Engine();
await engine.reload(modelId);
```