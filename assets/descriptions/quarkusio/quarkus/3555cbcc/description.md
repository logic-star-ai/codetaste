# Migrate reactive SQL client extensions from vendor-specific Pool types to generic Pool type

## Summary
Migrate reactive SQL client extensions (PostgreSQL, MySQL, MS SQL Server, Oracle, DB2) from vendor-specific pool types (`PgPool`, `MySQLPool`, etc.) to the generic `io.vertx.sqlclient.Pool` type to prepare for Vert.x 5 compatibility.

## Why
- Vendor-specific pool types (`PgPool`, `MySQLPool`, `MSSQLPool`, `OraclePool`, `DB2Pool`) are deprecated in Vert.x 4 and will be removed in Vert.x 5
- Need incremental migration path to avoid breaking changes

## Changes

### Documentation
- Replace vendor-specific pool type imports with `io.vertx.mutiny.sqlclient.Pool` 
- Remove "Pool class name" column from reactive SQL clients table
- Update all code examples to use generic `Pool` injection

### Deployment processors
- Create beans based on parent `Pool` type instead of vendor-specific types
- Add new `*PoolSupport` singleton beans to track which datasources belong to which vendor
- Deprecate vendor-specific build items (`PgPoolBuildItem`, `MySQLPoolBuildItem`, etc.) with `@Deprecated(forRemoval = true)`
- Introduce `ReactiveDataSourceDotNames` utility class with common constants

### Runtime
- Update `*PoolCreator` interfaces to return `Pool` instead of vendor-specific types
- Add `*PoolSupport` classes containing sets of pool names for each vendor
- Update recorders to:
  - Return generic `Pool` type from configurators
  - Cast to vendor-specific types only when needed (e.g., when calling driver APIs)
  - Create `*PoolSupport` runtime values

### Health checks
- Update health checks to filter pools by checking against vendor-specific pool name sets from `*PoolSupport` beans
- Iterate over generic `Pool` beans instead of vendor-specific types

### Integration tests
- Update all test resources to inject `Pool` instead of vendor-specific types
- Verify same pool instances are used across different injection points

## Affected Extensions
- `quarkus-reactive-pg-client`
- `quarkus-reactive-mysql-client`
- `quarkus-reactive-mssql-client`
- `quarkus-reactive-oracle-client`
- `quarkus-reactive-db2-client`