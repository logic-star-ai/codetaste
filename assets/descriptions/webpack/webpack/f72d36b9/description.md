# Introduce ChunkGraph to decouple chunk-module relationships

## Summary
Extract chunk↔module relationship management into dedicated `ChunkGraph` class, removing direct coupling between `Chunk` and `Module` objects.

## Why
- Improves separation of concerns by centralizing relationship management
- Enables lazy sorting of modules/chunks on demand vs. during compilation
- Reduces memory footprint by using WeakMaps instead of Sets on every object

## Changes

**Core Architecture:**
- Added `ChunkGraph` class with WeakMaps to track chunk↔module relationships
- Removed `_modules` field from `Chunk`, `_chunks` field from `Module`
- Added `compilation.chunkGraph` 
- Moved `connectChunkAndModule`/`disconnectChunkAndModule` from `GraphHelpers` to `ChunkGraph`
- Extracted comparator functions to `util/comparators`

**API Migration (Chunk):**
- `chunk.addModule/removeModule/containsModule` → `chunkGraph.connectChunkAndModule/disconnectChunkAndModule/isModuleInChunk`
- `chunk.getModules/modulesIterable` → `chunkGraph.getChunkModules/getChunkModulesIterable`
- `chunk.getNumberOfModules` → `chunkGraph.getNumberOfChunkModules`
- `chunk.compareTo` → `chunkGraph.compareChunks`
- `chunk.integrate` → `chunkGraph.integrateChunks`
- `chunk.getChunkModuleMaps` → `chunkGraph.getChunkModuleMaps`
- `chunk.hasModuleInGraph` → `chunkGraph.hasModuleInGraph`
- `chunk.size/modulesSize` → `chunkGraph.getChunkSize/getChunkModulesSize`
- ...

**API Migration (Module):**
- `module.addChunk/removeChunk/isInChunk` → (via `chunkGraph`)
- `module.getChunks/chunksIterable` → `chunkGraph.getModuleChunks/getModuleChunksIterable`
- `module.getNumberOfChunks` → `chunkGraph.getNumberOfModuleChunks`
- `module.hasEqualChunks` → `chunkGraph.haveModulesEqualChunks`
- `module.isEntryModule` → `chunkGraph.isEntryModule`
- ...

**Updated Subsystems:**
- All plugins/templates updated to use `chunkGraph` APIs
- `ModuleTemplate`, `ChunkTemplate`, `MainTemplate` render contexts include `chunkGraph`
- Stats generation updated
- HMR/optimization plugins updated
- WASM handling updated

## Breaking Changes
Many `Chunk`/`Module` methods removed or relocated to `ChunkGraph`. Plugins/loaders must access relationships via `compilation.chunkGraph`.