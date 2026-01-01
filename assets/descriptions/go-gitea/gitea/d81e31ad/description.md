# Refactor: Move db.Engine parameter to context.Context across codebase

## Summary
Refactor almost all database access functions to accept `context.Context` instead of `db.Engine` as their first parameter, enabling better request scoping, cancellation support, and more idiomatic Go patterns.

## Why
- **Context Propagation**: Using `context.Context` allows proper propagation of request lifecycles, timeouts, and cancellation signals through the database layer
- **Idiomatic Go**: Accepting `context.Context` as the first parameter is standard Go practice for functions that perform I/O operations
- **Code Deduplication**: Removes numerous wrapper functions that existed solely to call underlying functions with `db.GetEngine(db.DefaultContext)`
- **Request Scoping**: Enables database operations to be properly scoped to HTTP requests or background jobs

## Changes

### Function Signature Updates
- `func GetUserByName(name string)` → `func GetUserByName(ctx context.Context, name string)`
- `func GetIssueByID(id int64)` → `func GetIssueByID(ctx context.Context, id int64)`  
- `func GetLabelsByRepoID(repoID int64, ...)` → `func GetLabelsByRepoID(ctx context.Context, repoID int64, ...)`
- ...and ~200+ similar function signature changes

### Wrapper Function Removal
Removed unnecessary wrapper functions that just passed `db.DefaultContext`:
```go
// REMOVED
func GetUserByName(name string) (*User, error) {
    return getUserByName(db.GetEngine(db.DefaultContext), name)
}

// KEPT & RENAMED
func GetUserByName(ctx context.Context, name string) (*User, error) {
    // implementation using db.GetEngine(ctx)
}
```

### Database Access Pattern
Updated internal usage from:
```go
func someFunc(e db.Engine) { ... }
```
to:
```go
func someFunc(ctx context.Context) {
    e := db.GetEngine(ctx)
    ...
}
```

### Affected Modules
- `models/`: user, issue, comment, label, repo, mirror, notification, project, review, tracked_time, ...
- `models/asymkey/`: gpg_key, ssh_key, deploy_key, ...
- `models/auth/`: oauth2, ...
- `services/`: pull, issue, repository, auth, mirror, ...
- `routers/`: API v1 handlers, web handlers, private API, ...
- `modules/`: context, convert, indexer, ...
- Integration tests

### Helper Changes
- `db.Insert(ctx, ...)` instead of `e.Insert(...)`
- `db.GetByBean(ctx, ...)` instead of `e.Get(...)`
- `db.DeleteByBean(ctx, ...)` instead of `e.Delete(...)`
- `db.Exec(ctx, ...)` for raw SQL

## Migration Notes
- All callers must now pass a `context.Context` (typically `ctx`, `db.DefaultContext`, or `context.Background()`)
- Session/transaction management still uses `db.GetEngine(ctx)` internally
- Tests updated to pass `db.DefaultContext` where needed