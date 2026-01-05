# Refactor EVM ORMs to remove pg dependency

## Summary
Refactor Headtracker, Forwarder, and Logpoller ORMs to remove dependency on `core/services/pg` and `Q` type. Migrate to using `sqlutil.DB` interface and explicit context propagation.

## Why
- Decouple EVM services from the legacy `pg` package
- Standardize database access patterns across the codebase
- Improve context propagation throughout ORM methods
- Align with `sqlutil.DB` interface for better abstraction

## Changes

### ORM Refactoring
- **Headtracker ORM**: Renamed to `DbORM`, constructor now `NewORM(chainID big.Int, db sqlutil.DB)`, removed logger/config deps
- **Forwarder ORM**: Renamed to `DbORM`, constructor now `NewORM(db sqlutil.DB)`, added `Transaction()` method
- **Logpoller ORM**: Constructor now `NewORM(chainID *big.Int, db sqlutil.DB, lggr logger.Logger)`, removed `pg.QConfig`

### Method Signature Updates
- All ORM methods now accept `context.Context` as first parameter
- Removed `qopts ...pg.QOpt` variadic parameters throughout
- Changed from `pg.Q` methods (`ExecQ`, `Get`, `Select`) to `sqlutil.DB` context methods (`ExecContext`, `GetContext`, `SelectContext`)
- Updated cleanup function signatures: `func(pg.Queryer, ...) error` → `func(sqlutil.DB, ...) error`

### Interface Updates
- `LogPoller` interface methods: `Method(params, qopts ...pg.QOpt)` → `Method(ctx context.Context, params)`
- Config poller, event provider, transmitter methods similarly updated
- Job delegate `OnDeleteJob()` methods now accept `context.Context`

### Test Updates
- Tests updated to use `testutils.Context(t)` and pass context to ORM methods
- Mock method signatures updated to match new interfaces
- Removed `pg.WithParentCtx()` calls throughout tests

### Deprecation
- `pg.QOpt` marked as deprecated with migration guidance
- `pg.Queryer` marked as deprecated in favor of `sqlutil.DB`

### Miscellaneous  
- Moved `promSQLQueryTime` metric to `sqlutil` package
- Updated imports across ~100+ files
- Added context timeout for ORM cleanup operations
- Exported `DbORM` structs for direct instantiation