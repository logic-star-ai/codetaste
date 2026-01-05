# Title
-----
Refactor DBContext to standard Go context.Context

# Summary
-------
Remove special handling of `DBContext` and make it a standard Go `context.Context`. Replace `db.DefaultContext()` function with `db.DefaultContext` variable and introduce `db.GetEngine(ctx)` helper to retrieve database engine from any context.

# Why
---
Current implementation has `DBContext` as a special type with direct engine access, limiting flexibility. By making it a standard context, we can:
- Simplify engine retrieval to work with any context
- Prepare for future context-aware database operations
- Reduce special-casing throughout the codebase
- Follow Go idioms for context handling

# Changes
---------
**Core (`models/db/context.go`)**:
- `DefaultContext` changed from `func() *Context` → `var DefaultContext context.Context`
- `Context` now embeds `context.Context`
- Added `Engined` interface for types providing engine access
- Added `GetEngine(ctx context.Context) Engine` helper
- Added `NewSession(ctx context.Context) *xorm.Session` helper
- `WithTx()` signature: `func(*Context)` → `func(context.Context)`
- `Iterate()`, `Insert()` signatures: `*Context` → `context.Context`

**Throughout codebase**:
- `db.DefaultContext().Engine()` → `db.GetEngine(db.DefaultContext)`
- `db.DefaultContext().NewSession()` → `db.NewSession(db.DefaultContext)`
- `ctx.Engine()` → `db.GetEngine(ctx)` (inside functions)
- Function signatures: `*db.Context` → `context.Context` parameters
- Error message typo fix: "Attachement" → "attachment"

**Pattern**:
```go
// Before
func DoSomething(ctx *db.Context, ...) {
    result, err := ctx.Engine().Find(...)
}

// After  
func DoSomething(ctx context.Context, ...) {
    result, err := db.GetEngine(ctx).Find(...)
}
```

# Files affected
---------------
- `models/db/context.go` - Core refactoring
- `models/db/engine.go` - DefaultContext initialization
- `models/db/unit_tests.go` - Test context setup
- `models/*.go` - ~100+ model files updated
- `modules/repository/*.go` - Repository operations
- `routers/web/**/*.go` - Web handlers
- `services/**/*.go` - Service layer