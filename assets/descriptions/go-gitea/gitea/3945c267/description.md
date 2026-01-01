# Refactor template functions to accept explicit context parameter

## Summary

Remove `db.DefaultContext` usage from functions called in templates. These functions now require an explicit `context.Context` parameter instead of using the default context internally.

## Why

- Part of broader effort to eliminate `db.DefaultContext` (#27065)
- Makes context propagation explicit throughout the codebase
- Improves traceability and allows proper context cancellation/timeout handling
- Aligns with Go best practices for context management

## Changes

**Affected areas:**
- `models/activities/*` - Action, Notification methods (GetActFullName, GetRepoLink, HTMLURL, etc.)
- `models/issues/*` - Comment, Review, Issue methods (HTMLURL, Link, LoadLabel, LoadProject, etc.)
- `models/project/*` - Project, Board methods (Link, NumIssues, etc.)
- `models/repo/*` - Mirror, Collaboration methods (GetRepository, IsOwnerMemberCollaborator, etc.)
- `services/*` - Various service layer functions
- `templates/**/*.tmpl` - All template files calling these methods

**Pattern:**
```go
// Before
func (a *Action) GetActFullName() string {
    a.LoadActUser(db.DefaultContext)
    ...
}

// After  
func (a *Action) GetActFullName(ctx context.Context) string {
    a.LoadActUser(ctx)
    ...
}
```

**Template changes:**
```html
<!-- Before -->
<a href="{{.GetRepoLink}}">...</a>

<!-- After -->
<a href="{{.GetRepoLink ctx}}">...</a>
```

## Risk

⚠️ **High risk** - Templates are not statically typed. Errors are harder to catch at compile time. Missing `ctx` parameters in templates will cause runtime failures.

## Testing needed

- Comprehensive manual testing of all affected templates
- Community testing recommended
- Check all dashboard feeds, notification pages, issue/PR views, project boards, etc.