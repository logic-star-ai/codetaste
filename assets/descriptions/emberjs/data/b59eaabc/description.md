# Consolidate @warp-drive/core-types and @ember-data/request into @warp-drive/core

## Summary

Migrate type definitions from `@warp-drive/core-types` and request functionality from `@ember-data/request` into a unified `@warp-drive/core` package. Maintain backward compatibility by converting legacy packages to re-export from new locations.

## Why

- **Reduce fragmentation**: Consolidate related core functionality into single package
- **Improve organization**: Centralize types and request logic under `warp-drive-packages/core/`
- **Cleaner architecture**: Reduce package count and simplify dependency graph
- **Better maintainability**: Single source of truth for core types and request functionality

## Changes

### Package Migration

**Source Packages**:
- `packages/core-types/src/**` → `warp-drive-packages/core/src/types/**`
- `@ember-data/request` → `warp-drive-packages/core/src/request.ts`

**Backward Compatibility**:
- `packages/core-types/src/` files converted to re-exports from `@warp-drive/core/types/...`
- All exports maintained via delegation pattern

### File Structure

**New Structure**:
```
warp-drive-packages/core/
├── src/
│   ├── types/
│   │   ├── cache/
│   │   ├── json/
│   │   ├── schema/
│   │   ├── spec/
│   │   ├── -private.ts
│   │   ├── cache.ts
│   │   ├── graph.ts
│   │   ├── identifier.ts
│   │   ├── params.ts
│   │   ├── record.ts
│   │   ├── request.ts
│   │   ├── runtime.ts
│   │   ├── symbols.ts
│   │   └── utils.ts
│   ├── index.ts
│   └── request.ts
├── tsconfig.json
├── vite.config.mjs
└── typedoc.config.mjs
```

### Configuration Updates

**Build & Types**:
- Add TypeScript project at `warp-drive-packages/core/tsconfig.json`
- Configure Vite entrypoints for all exported modules
- Update TypeDoc to include new package location
- Add `declarations` to `.gitignore` for generated types
- Exclude `warp-drive-packages/core/types` from prettier

**Dependencies**:
- Add `@warp-drive/core` peer dep to `@warp-drive/core-types`
- Add `@ember/test-waiters` as external dependency

### Entry Points

Exposed modules include:
- `@warp-drive/core` → main index
- `@warp-drive/core/request` → request functionality  
- `@warp-drive/core/types/**` → all type exports (cache, schema, spec, etc.)
- `@warp-drive/core/types/-private` → internal utilities
- `@warp-drive/core/types/runtime` → runtime config

### Type Reorganization

All types from:
- `cache/` → aliases, changes, mutations, operations, relationships
- `json/` → raw value types
- `schema/` → concepts, fields
- `spec/` → document, error, json-api-raw
- Root types → graph, identifier, params, record, request, symbols, utils

## Notes

- Legacy packages remain functional via re-export pattern
- No breaking changes to public APIs
- Build tooling consolidated under single package configuration
- Turbo cache tweaks for improved build performance