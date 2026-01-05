# Refactor: Replace `*kri.Identifier` with value-based `kri.Identifier` in policy logic

## Summary

Replace pointer-based `*kri.Identifier` with value-based `kri.Identifier` throughout policy handling code to simplify the API, eliminate unnecessary pointer handling, and improve code consistency.

## Why

Current codebase uses `*kri.Identifier` in policy handling, which:
- Introduces unnecessary pointer handling complexity
- Makes code less consistent
- Obscures the origin of references in matchers, resolvers, and route generators
- Requires nil checks and pointer dereferencing throughout

## Changes Required

**Core identifier handling:**
- Replace all `*kri.Identifier` with `kri.Identifier` across policy system
- Add `IsEmpty()` method to check for empty identifiers
- Update nil checks to use `IsEmpty()` instead

**Function signature simplification:**
- Remove `sectionName` parameter from `kri.From()` and `kri.FromResourceMeta()`
- Introduce `kri.WithSectionName(...)` helper for setting section names (supports both string and numeric names)
- Ensure `WithSectionName()` avoids modifying empty identifiers

**Reference resolution:**
- Update `TargetRef` and `BackendRef` resolution to use `kri.Identifier` directly instead of `core_model.ResourceMeta`
- Update `BackendRef()` to accept `kri.Identifier` origin instead of `core_model.ResourceMeta`
- Update `TargetRefToKRI()` to accept `kri.Identifier` origin

**Resource types affected:**
- `core_xds.Resource.ResourceOrigin`: `*kri.Identifier` → `kri.Identifier`
- `xds_types.Outbound.Resource`: `*kri.Identifier` → `kri.Identifier`
- `xds_types.ExternalService.OwnerResource`: `*kri.Identifier` → `kri.Identifier`
- `resolve.RealResourceBackendRef.Resource`: `*kri.Identifier` → `kri.Identifier`

**Method updates:**
- `ResourceOrNil()` → `Resource()` returning `kri.Identifier` instead of `*kri.Identifier`
- Update all callers to check `IsEmpty()` instead of nil

**Test updates:**
- Update all test fixtures to use value-based identifiers
- Remove `pointer.To()` calls for KRI construction

## Scope

Files affected:
- `pkg/core/kri/kri.go`
- `pkg/core/xds/...`
- `pkg/plugins/policies/core/rules/...`
- `pkg/plugins/policies/*/plugin/...`
- `pkg/xds/...`
- All related tests