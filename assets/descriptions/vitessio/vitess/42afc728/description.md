# Refactor out more usage of servenv for mysql version

## Summary
Remove dependency on `servenv.MySQLServerVersion()` throughout the codebase by passing MySQL version as an explicit parameter instead of accessing it globally.

## Why
- Makes `evalengine` and `schemadiff` more standalone with fewer transitive dependencies
- Reduces coupling to `servenv` package
- Enables easier library reuse with smaller binary sizes
- Makes dependencies explicit and testable

## What Changed
- Added `mysqlVersion string` parameter/field to structs and functions across:
  - `vtgate/evalengine/...`
  - `vttablet/tabletserver/...`
  - `vtctl/workflow/...`
  - `vtadmin/...`
  - `wrangler/...`
  - `schemadiff/...`
- MySQL version now obtained once at initialization (via `servenv.MySQLServerVersion()`) and passed through call chains
- Removed `servenv.SetMySQLServerVersionForTest()` helper
- Updated tests to use `config.DefaultMySQLVersion` directly
- Added `MySQLVersion() string` method to various interfaces (`VCursor`, `Env`, `SchemaInformation`, etc.)

## Impact
- Breaking API changes to many function signatures
- Libraries like `evalengine` and `schemadiff` now have significantly fewer dependencies
- Better separation of concerns and reduced coupling