# Title

Remove circular dependency between Env and PushContext

## Summary

Refactor `PushContext` to eliminate circular dependency with `Environment`. `PushContext` now directly contains mesh config, networks config, and service/config store interfaces instead of referencing `Environment`.

## Why

- **Pure snapshot semantics**: `PushContext` should be a pure snapshot of environment state at push start
- **Prevent mid-push mutations**: Conversion logic no longer has direct access to `Environment`, preventing mesh/network config changes during push
- **Cleaner architecture**: Breaks circular dependency between `Env` and `PushContext`

## Changes

- Move `Mesh`, `Networks`, `ServiceDiscovery`, `IstioConfigStore` from `Environment` reference to direct fields in `PushContext`
- Remove `Env *model.Environment` from plugin `InputParams`
- Update all conversion functions to accept `*model.PushContext` instead of `*model.Environment`
  - `BuildClusters()`, `BuildListeners()`, `BuildHTTPRoutes()`
  - `buildGatewayListeners()`, `buildSidecarOutboundListeners()`, etc.
  - Network filter builders, TLS filter chain builders, etc.
- Change access patterns:
  - `pluginParams.Env.Mesh` → `pluginParams.Push.Mesh`
  - `env.Mesh.SdsUdsPath` → `push.Mesh.SdsUdsPath`
  - `env.MeshNetworks` → `push.Networks`
  - etc.
- Move `ReadMeshConfig()` and `ReadMeshNetworks()` from `pilot/cmd/cmd.go` to `pkg/config/mesh/mesh.go`
- Move `ResolveHostsInNetworksConfig()` from `pilot/pkg/networking/util` to `pkg/config/mesh`
- Update all tests to populate `PushContext` fields directly

## Scope

Across pilot networking core (v1alpha3), plugins (authn, authz, mixer, health), gateway/listener/cluster builders, and configuration loading.