# Title

Continue `db.DefaultContext` removal - propagate context to model functions

# Summary

Refactor model layer functions to accept `context.Context` parameter instead of hardcoding `db.DefaultContext` internally.

# Why

- Hardcoded `db.DefaultContext` prevents proper timeout/cancellation/tracing
- Blocks context propagation throughout request lifecycle  
- Makes testing and monitoring harder
- Violates Go best practices for context handling

# Changes

**Pattern**: `Func(...) error` → `Func(ctx context.Context, ...) error`

**Remove wrapper functions** that only passed `db.DefaultContext`:
```go
// Before
func LoadRepo() error { return loadRepo(db.DefaultContext) }
func loadRepo(ctx context.Context) error { ... }

// After  
func LoadRepo(ctx context.Context) error { ... }
```

**Affected areas**:
- `models/actions/*` - schedule queries
- `models/admin/task.go` - migration task operations  
- `models/auth/*` - session + webauthn credential management
- `models/issues/*` - labels, milestones, stopwatch, issue watching
- `models/organization/*` - org list queries
- `models/repo/*` - archiver, topics, transfers, updates
- `models/user/*` - follow operations
- `models/repo_transfer.go` - transfer validation
- Service layers - issue labels, migrations, repository ops, tasks
- Routers/handlers - pass context from HTTP requests

**Call sites**: Update ~200+ call sites to pass `ctx` or `db.DefaultContext` appropriately.

# Related

Part of #27065 - broader effort to eliminate all hardcoded context usage.