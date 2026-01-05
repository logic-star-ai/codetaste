Title
-----
Reorganize v1alpha1 test utilities into dedicated sub-package

Summary
-------
Consolidate v1alpha1-specific test utilities under `test/v1alpha1/` sub-package to improve code organization and prepare for multi-version API support.

Why
---
- v1alpha1 utilities were scattered across the main `test/` package
- Difficult to distinguish version-specific helpers from generic test utilities
- Naming confusion between general serving clients and v1alpha1-specific clients
- Need better separation as the project evolves toward newer API versions

Changes
-------
**Package Structure:**
- Created new `test/v1alpha1/` sub-package for v1alpha1-specific utilities
- Moved `configuration.go`, `service.go`, `route.go`, `revision.go` to `test/v1alpha1/`
- Moved API conformance tests from `test/conformance/api/` → `test/conformance/api/v1alpha1/`
- Created `test/v1alpha1/crd.go` for resource objects and helper types

**Naming Updates:**
- `ServingClients` → `ServingAlphaClients`
- `ServingClient` → `ServingAlphaClient`
- Consistent use of `v1a1test` import alias for the new package

**Function Consolidation:**
- `foo`-related functions grouped under `test/v1alpha1/foo.go` (e.g., Configuration*, Route*, Service*, Revision*)
- Split `states.go` functions across appropriate resource files (IsRevisionReady → revision.go, IsServiceReady → service.go, ...)
- Moved state checking functions: `WaitFor*State`, `Check*State`, `Is*Ready` to respective resource files

**Updated Test Files:**
- e2e tests (`test/e2e/*.go`)
- Performance tests (`test/performance/*.go`)
- Scale tests
- Upgrade tests (`test/upgrade/*.go`)
- Runtime conformance tests (import path updates)

Files
-----
**Created:**
- `test/v1alpha1/configuration.go` - Configuration utilities
- `test/v1alpha1/service.go` - Service utilities  
- `test/v1alpha1/route.go` - Route utilities
- `test/v1alpha1/revision.go` - Revision utilities
- `test/v1alpha1/crd.go` - Common types (ResourceObjects, Options, ...)

**Moved:**
- `test/conformance/api/*.go` → `test/conformance/api/v1alpha1/*.go`

**Deleted:**
- `test/configuration.go`
- `test/service.go` (functions moved)
- `test/route.go` (functions moved)
- `test/states.go` (split across resource files)

**Modified:**
- `test/clients.go` - Client type renaming
- `test/cleanup.go` - Use `ServingAlphaClient`
- `test/crd_checks.go` - Removed state functions (moved to v1alpha1)
- `test/crd.go` - Removed resource constructors (moved to v1alpha1)
- All test files importing v1alpha1 utilities