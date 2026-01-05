# Remove evm/config/v2 versioning; reorganize into config and config/toml packages

## Summary
Refactor `core/chains/evm/config` package structure to eliminate v2 versioning and improve organization by splitting into interface/implementation (`config`) and TOML type definitions (`config/toml`) packages.

## Why
- v2 versioning in package path is unnecessary and creates confusion
- Better separation of concerns: interfaces/implementations vs TOML struct definitions
- Clearer, more maintainable package structure

## Changes

### Package Restructure
- Rename `evm/config/v2` → split into two packages:
  - `evm/config` - interfaces + `ChainScoped` implementation
  - `evm/config/toml` - TOML struct types + defaults

### File Movements
- `chain_scoped*.go` files → `evm/config/`
- `config.go`, `defaults.go`, `defaults/**/*.toml` → `evm/config/toml/`
- Remove `config_node_pool.go` (consolidated)

### Code Updates
- Update package declarations: `package v2` → `package config` or `package toml`
- Update imports throughout codebase:
  - `v2 "...evm/config/v2"` → `"...evm/config/toml"`
  - References to `v2.*` → `config.*` or `toml.*`
- Update function signatures + type references
- Update test files accordingly