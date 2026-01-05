# Refactor SD configuration to remove `config` dependency

## Summary
Restructure service discovery (SD) configuration to decouple discovery packages from the main `config` package, improving modularity and reusability.

## Why
- Discovery packages currently depend on `config` via `config.TargetGroup` and SD config structs
- This creates tight coupling and hinders reusability
- Better separation of concerns needed between configuration and discovery logic

## Changes

**New Packages:**
- `discovery/targetgroup` - contains `TargetGroup` struct (moved from `config`)
- `discovery/config` - contains `ServiceDiscoveryConfig` aggregating all SD configs
- `util/config` - common config utilities (`HTTPClientConfig`, `TLSConfig`, `BasicAuth`, `Secret`, `URL`)
- `util/yaml` - YAML utilities (`CheckOverflow()`)

**SD Config Structs Moved:**
- `DNSSDConfig` → `discovery/dns`
- `FileSDConfig` → `discovery/file`
- `ConsulSDConfig` → `discovery/consul`
- `MarathonSDConfig` → `discovery/marathon`
- `KubernetesSDConfig` → `discovery/kubernetes`
- `EC2SDConfig` → `discovery/ec2`
- `GCESDConfig` → `discovery/gce`
- `AzureSDConfig` → `discovery/azure`
- `OpenstackSDConfig` → `discovery/openstack`
- `TritonSDConfig` → `discovery/triton`
- `ServersetSDConfig`, `NerveSDConfig` → `discovery/zookeeper`

**Updated:**
- All imports across retrieval, notifier, storage, tests
- Discovery manager to use new package structure
- Main config package to import from `discovery/config` and `util/config`

## Result
- Discovery packages are now self-contained with their own configs
- `config` package only imports discovery packages, not vice versa
- Improved modularity and potential for external reuse