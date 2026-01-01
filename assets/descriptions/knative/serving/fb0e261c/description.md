# Rename `pkg/controller` to `pkg/reconciler`

## Summary
Rename `pkg/controller` package to `pkg/reconciler` to better reflect that it contains Reconciler implementations (from `github.com/knative/pkg/controller.Reconciler` interface), not controller implementations.

## Why
The current package name is misleading. These packages implement the `Reconciler` interface while the actual controller logic lives in `github.com/knative/pkg/controller`.

## Changes
- Move `pkg/controller/*` → `pkg/reconciler/v1alpha1/*`
- Incorporate API version (`v1alpha1`) into reconciler import paths
- Update all import statements across:
  - `cmd/activator`
  - `cmd/controller`  
  - `cmd/multitenant-autoscaler`
  - `pkg/activator`
  - `pkg/autoscaler`
  - Test files
- Update `hack/update-codegen.sh` to reference new paths
- Add package documentation to `pkg/reconciler/doc.go` explaining:
  - What reconcilers are
  - Their relationship to controllers
  - Expected constructor pattern: `NewController(...) *controller.Impl`
- Update `.gitattributes` coverage exclusion: `/pkg/controller/testing/**` → `/pkg/**/testing/**`
- Remove redundant import aliases