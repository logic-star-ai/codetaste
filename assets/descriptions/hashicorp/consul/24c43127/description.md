# Refactor: Decouple troubleshoot module from consul top-level module

## Summary
Refactor troubleshoot into an independent Go module to enable import into consul-k8s without pulling in all of consul's dependencies. Create new `envoyextensions` module for shared code between xds and troubleshoot packages.

## Background
The troubleshoot module needs to be importable by consul-k8s, but currently depends on consul's top-level module. This creates circular dependencies and pulls in unnecessary code.

## Changes

### New Go Modules
- Convert `troubleshoot/` to standalone go module
- Create `envoyextensions/` go module for shared xds-related code
  - Contains `xdscommon/` and `extensioncommon/` packages
  - Both xds and troubleshoot can import without circular deps

### Code Movement
- `agent/xds/xdscommon/` → `envoyextensions/xdscommon/`
- `agent/xds/proxysupport/` → `envoyextensions/xdscommon/` (merged)
- `agent/envoyextensions/extensioncommon/` → `envoyextensions/extensioncommon/`
- `agent/envoyextensions/builtin/validate/` → `troubleshoot/validate/`
- Troubleshoot code reorganized under `troubleshoot/proxy/`
- Tests with proxycfg/xds dependencies → `agent/xds/validateupstream-test/` (with explanation comment)

### Breaking Changes
- `extensioncommon.UpstreamData` now pointer in maps: `map[...]*UpstreamData`
- All imports updated throughout codebase

### CI/Testing
- Add linting for envoyextensions + troubleshoot modules
- Add go-test-lib jobs for both modules in CircleCI
- Maintain full test coverage with reorganized tests

## Why
- Enable consul-k8s to import troubleshoot without consul dependency
- Improve modularity and separation of concerns
- Share common Envoy-related code across packages
- Reduce coupling between components