# Title
-----
Move provisioners to dedicated package to avoid circular dependencies

# Summary
-------
Extract all provisioner-related code from `pkg/e2e` and `pkg/environments` into a new dedicated `pkg/provisioners` package to enable cleaner separation of concerns and avoid circular dependencies.

# Why
---
Currently, provisioners are split between `pkg/e2e` and `pkg/environments`, creating tight coupling and preventing environments from implementing a `Diagnosable` interface (needed to dump agent logs and config at test failure time) due to circular dependency issues.

# Changes
--------
**Package Structure:**
- Create new package: `test/new-e2e/pkg/provisioners/`
- Move provisioner core types from `pkg/e2e/`:
  - `provisioner.go` → `provisioners/provisioners.go`
  - `pulumi_provisioner.go` → `provisioners/pulumi_provisioner.go`
  - `file_provisioner.go` → `provisioners/file_provisioner.go`
- Move all provider implementations from `pkg/environments/...` to `pkg/provisioners/...`:
  - `environments/aws/...` → `provisioners/aws/...`
  - `environments/azure/...` → `provisioners/azure/...`
  - `environments/gcp/...` → `provisioners/gcp/...`
  - `environments/local/...` → `provisioners/local/...`

**Types Moved:**
- `Provisioner`, `TypedProvisioner[Env]`, `UntypedProvisioner`
- `PulumiEnvRunFunc[Env]`
- `ProvisionerMap`, `RawResources`
- `Diagnosable` interface
- Helper functions: `CopyProvisioners()`, `RawResources.Merge()`

**Import Updates:**
- Update ~100+ test files to import from `pkg/provisioners` instead of `pkg/e2e` or `pkg/environments`
- Update provisioner instantiation calls (`e2e.NewTypedPulumiProvisioner` → `provisioners.NewTypedPulumiProvisioner`, etc.)

**Cleanup:**
- Rename `environments/doc.go` → `environments/environments.go`

# Impact
-------
- **Breaking Change**: All tests using provisioners need import updates
- **Benefits**: 
  - Cleaner separation of concerns
  - Enables future `Diagnosable` interface on environments
  - Resolves circular dependency issues
- **No Functional Changes**: Pure code movement/refactoring

# Related
--------
Part 1 of refactoring to enable environment diagnostics at test failure time.