# Refactor Galley Schema Model for Pilot/Galley Convergence

## Summary
Major refactoring of Galley's schema model to enable merging with Pilot's schema system. Consolidates resource/collection definitions and eliminates kube-specific source abstractions.

## Changes

### Schema Architecture
- **Removed `sources` abstraction** from metadata
  - Only kube source existed; kube metadata (kind/group/version) now directly in resource schema
  - Eliminated unnecessary indirection for Kubernetes-specific resources
  
- **Introduced top-level `resource.Schema`** in `metadata.yaml`
  - Defines all resource types known to Istio
  - Single source of truth for resource definitions

- **Refactored `collection.Schema`**
  - Now references `resource.Schema` + collection name + `disabled` flag
  - Collections become first-class objects vs. just names
  - Methods: `.Name()`, `.Kind()`, `.Proto()`, `.Group()`, etc.

### Code Generation
- Codegen now produces **instance variables** for `collection.Schema` (not just names)
  - Example: `IstioNetworkingV1Alpha3Virtualservices` is now a `collection.Schema` instance
  - Required for Pilot integration
  
- Validation functions now **registered and retrievable**
  - `registerValidateFunc()` / `GetValidateFunc()` / `IsValidateFunc()`
  - Enables dynamic validation lookup

### Structure
```
galley/pkg/config/meta/metadata → galley/pkg/config/schema
├── collections/     # Generated collection instances
├── snapshots/       # Snapshot definitions  
├── resource/        # Resource schema
└── collection/      # Collection schema
```

### API Changes
- Collection references: `metadata.Collection1` → `collections.Collection1.Name()`
- Immutable schema references throughout
- Builder patterns: `collection.NewSchemasBuilder()`, `resource.Builder{...}.Build()`

## Why
- **Pilot/Galley convergence**: Align schema models between components
- **Simplification**: Remove unnecessary kube-specific abstraction layer
- **Type safety**: Full schema objects vs. string-based collection names
- **Extensibility**: Registered validation functions, cleaner resource definitions

## Affected Areas
- All analysis analyzers (updated collection references)
- MCP backend (schema mapping)
- Source analyzers (kuberesource filtering)
- Validation (function registration)
- Tests (schema/collection access patterns)