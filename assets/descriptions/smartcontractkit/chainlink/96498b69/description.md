# Title
Migrate integration-test utilities to chainlink-testing-framework

# Summary
Refactor integration tests to use utilities from `chainlink-testing-framework` (v1.19.0) instead of local implementations. This involves moving common helper functions, config builders, and test utilities to the shared testing framework.

# Why
- Reduce code duplication across integration tests
- Centralize common testing utilities in CTF for better maintainability
- Enable shared utilities across multiple Chainlink repositories
- Improve consistency in test infrastructure

# Changes

## Import Path Migrations
- `integration-tests/utils` → `chainlink-testing-framework/utils/{conversions,ptr,testcontext}`
- `integration-tests/client` → `chainlink-testing-framework/networks`
- `integration-tests/utils` → `chainlink-testing-framework/utils/osutil`

## Function Renames
- `utils.Ptr()` → `ptr.Ptr()`
- `utils.EtherToWei()` → `conversions.EtherToWei()`
- `utils.TestContext(t)` → `testcontext.Get(t)`
- `utils.GetEnv()` → `osutil.GetEnv()`
- `client.AddNetworksConfig()` → `networks.AddNetworksConfig()`
- `client.AddNetworkDetailedConfig()` → `networks.AddNetworkDetailedConfig()`

## Deleted Files
- `integration-tests/client/chainlink_config_builder.go` (moved to CTF)
- Utility functions from `integration-tests/utils/common.go` (moved to CTF)

## Updated Dependencies
- Bump `chainlink-testing-framework` from v1.18.6 to v1.19.0

# Affected Areas
- All integration test files using common utilities
- Docker test environments
- Chaos tests
- Smoke tests
- Performance tests
- Load tests
- Benchmark tests
- Configuration builders