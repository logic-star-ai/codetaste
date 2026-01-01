# Refactor: Move migration and seed code into Driver layer

## Summary
Consolidate database migration and seed logic from `store/db` package into the `store/sqlite` driver implementation. Eliminate the `store/db.DB` abstraction by merging its responsibilities directly into `Driver`.

## Why
- Current architecture has unnecessary layering: `db.DB` → `Driver` → `Store`
- Migration/seed logic is database-specific and belongs in driver implementations
- Simplifies initialization flow (no separate open → migrate → create driver steps)
- Cleaner separation of concerns

## Changes

### Package Restructure
- **Remove** `store/db` package entirely
- **Move** `store/db/db.go` → `store/sqlite/migrate.go`
- **Move** `store/db/migration_history.go` → `store/sqlite/migration_history.go`
- **Move** migration SQL files: `store/db/migration/**/*.sql` → `store/sqlite/migration/**/*.sql`
- **Move** seed SQL files: `store/db/seed/**/*.sql` → `store/sqlite/seed/**/*.sql`

### Driver Interface
Add `Migrate(ctx context.Context) error` to `store.Driver` interface

### SQLite Driver
- Change constructor signature: `NewDriver(profile *profile.Profile) (store.Driver, error)`
- Handle DB connection opening internally
- Implement all migration/seed logic as driver methods
- Move `MigrationHistory*` methods to SQLite driver

### Initialization Flow
**Before:**
```go
db := db.NewDB(profile)
db.Open()
db.Migrate(ctx)
driver := sqlite.NewDriver(db.DBInstance)
store := store.New(driver, profile)
```

**After:**
```go
driver := sqlite.NewDriver(profile)
driver.Migrate(ctx)
store := store.New(driver, profile)
```

### Files to Update
- `cmd/memos.go` - simplified initialization
- `cmd/mvrss.go` - simplified initialization  
- `cmd/setup.go` - simplified initialization
- `test/server/server.go` - test server setup
- `test/store/store.go` - test store setup