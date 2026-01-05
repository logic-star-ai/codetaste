# Refactor codegen to eliminate global dependencies and improve architecture

## Summary
Refactor code generation architecture to remove global state dependencies and improve maintainability across service, HTTP, and gRPC codegen packages.

## Why
- Global `expr.Root` references make code harder to test and understand
- Confusing `ServicesData` naming where transport and service layers used similar structures
- `ServicesData` containing a `ServiceData` field created unclear boundaries
- Excessive boilerplate when initializing service data structures

## Changes

### Remove global root expression dependencies
- Update function signatures to accept `root *expr.RootExpr` as parameter
- Replace all `expr.Root` references with passed root parameter
- Ensure generated code correctly references API structure without globals

### Restructure ServicesData architecture
- Embed `service.ServicesData` in `http.ServicesData` and `grpc.ServicesData`
- Rename service maps to `HTTPServices`/`GRPCServices` for clarity
- Add `NewServicesData()` constructor functions to reduce initialization boilerplate
- Update variable names (`serviceData` → `services`) for semantic accuracy
- Clear separation between service layer and transport layer data structures

### Streamline file generation
- Consolidate file appending in `Service()` function
- Simplify section template creation in `EndpointFile()` and `ViewsFile()`
- Add `IsAliased` and `ServiceTypeRef` fields to `ServiceData` for better type resolution
- Update request initialization templates to utilize new fields

## Impact
- No changes required for existing Goa applications (backward compatible)
- Improved testability through elimination of global state
- Clearer code organization and naming conventions
- Better type resolution for aliased types
- Reduced cognitive load when navigating codebase