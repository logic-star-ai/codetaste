# Refactor `db.DefaultContext` usage to accept context parameters

## Summary
Refactor functions across models, services, and routers to accept `context.Context` as a parameter instead of using hardcoded `db.DefaultContext` internally. This enables proper context propagation for cancellation, deadlines, and tracing.

## Why
- Using `db.DefaultContext` prevents proper context propagation through the call stack
- Makes it impossible to cancel operations or enforce timeouts from callers
- Hinders distributed tracing and request-scoped logging
- Part of ongoing effort to improve context handling (#27065)

## Scope
**Models affected:**
- `asymkey` - GPG keys, SSH keys, public key regeneration
- `activities` - User heatmap data retrieval
- `issues` - Reactions, reviews, issue statistics, pull requests
- `organization` - Team search operations
- `repo` - Releases, tags, migrations
- `system` - System notices
- `user` - User redirects

**Services affected:**
- `asymkey` - Deploy key & SSH key deletion
- `auth` - External account linking
- `externalaccount` - Migration updates by type
- `migrations` - Repository syncing
- `packages` - All package type handlers (Alpine, Cargo, Chef, Composer, Conan, Conda, Container, CRAN, Debian, Generic, Go, Helm, Maven, npm, NuGet, Pub, PyPI, RPM, RubyGems, Swift, Vagrant)
- `release` - Release updates
- `repository` - Tag syncing, deletion checks

**API/Web routers affected:**
- Package upload/deletion endpoints
- Release management
- Reaction handling (issues/comments)
- Key management (GPG, SSH, deploy keys)
- User profile heatmaps
- Notice management

## Changes
Pattern consistently applied:
```go
// Before
func SomeFunction(...) error {
    return db.GetEngine(db.DefaultContext).Where(...)
}

// After  
func SomeFunction(ctx context.Context, ...) error {
    return db.GetEngine(ctx).Where(...)
}
```

- ~100+ function signatures updated to accept `context.Context`
- All callers updated to pass context down
- Tests updated to use `db.DefaultContext` when no request context available
- HTTP handlers pass `ctx` from request context

## Notes
- No functional changes, purely refactoring
- Maintains backward compatibility where needed via context propagation
- Sets foundation for future cancellation/timeout improvements