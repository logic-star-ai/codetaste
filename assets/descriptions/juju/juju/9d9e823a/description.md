# Title
-------
Remove juju/errors dependency from core package

# Summary
--------
Remove `juju/errors` from the core package and replace with internal error handling (`core/errors` and `internal/errors`). Migrate to Go 1.13+ error wrapping patterns.

# Why
-----
- Eliminate external dependency on `juju/errors` in core
- Standardize error handling across the codebase
- Leverage Go 1.13+ error wrapping (%w) and unwrapping
- Use typed error checking instead of `errors.Cause(...)`

# Changes
---------

## Error Handling Patterns

Replace `juju/errors` patterns:

- `errors.Trace(err)` → `errors.Capture(err)`
- `errors.Annotate(err, msg)` → `errors.Errorf(msg + ": %w", err)`
- `errors.Annotatef(err, fmt, ...)` → `errors.Errorf(fmt + ": %w", ..., err)`
- `errors.NotValidf(fmt, ...)` → `errors.Errorf(fmt + " %w", ..., coreerrors.NotValid)`
- `errors.NotFoundf(fmt, ...)` → `errors.Errorf(fmt + " %w", ..., coreerrors.NotFound)`
- `errors.NotSupportedf(fmt, ...)` → `errors.Errorf(fmt + " %w", ..., coreerrors.NotSupported)`
- `errors.BadRequestf(...)` → `errors.Errorf(...).Add(coreerrors.BadRequest)`
- `errors.Forbiddenf(...)` → `errors.Errorf(...).Add(coreerrors.Forbidden)`
- `errors.QuotaLimitExceededf(...)` → `errors.Errorf(...).Add(coreerrors.QuotaLimitExceeded)`
- `errors.NewNotValid(nil, msg)` → `errors.New(msg).Add(coreerrors.NotValid)`
- `errors.NewNotFound(nil, msg)` → `errors.New(msg).Add(coreerrors.NotFound)`
- `errors.NewNotSupported(nil, msg)` → `errors.New(msg).Add(coreerrors.NotSupported)`
- `errors.Cause(err)` → Direct error or `errors.AsType[T](err)`
- `errors.Hide(...)` → Remove (use `.Add(...)` instead)
- `os.IsNotExist(err)` → `errors.Is(err, fs.ErrNotExist)`
- `errors.Err` / `*errors.Err` → `error`

## Error Constants

Replace sentinel errors:
- `errors.NotValid` → `coreerrors.NotValid`
- `errors.NotFound` → `coreerrors.NotFound`
- `errors.NotSupported` → `coreerrors.NotSupported`
- `errors.AlreadyExists` → `coreerrors.AlreadyExists`
- `errors.NotProvisioned` → `coreerrors.NotProvisioned`
- `errors.BadRequest` → `coreerrors.BadRequest`
- `errors.Forbidden` → `coreerrors.Forbidden`
- `errors.QuotaLimitExceeded` → `coreerrors.QuotaLimitExceeded`

## Import Updates

Update imports throughout:
```go
- "github.com/juju/errors"
+ "github.com/juju/juju/core/errors"        // for error constants
+ "github.com/juju/juju/internal/errors"   // for error construction
```

## Automation

Scripts in `scripts/errors-patch/` automate most changes:
- Coccinelle-style patches for pattern matching/replacement
- Sed post-processing for string formatting cleanup
- Manual changes required for import tests

## Special Cases

- `apiserver/errors/errors.go`: Handle ConstError wrapping for leadership/lease
- `rpc/params/apierror.go`: Preserve `errors.Cause(...)` for httprequest compatibility
- Type assertions updated to use `errors.AsType[T](err)`

## Files Changed
- ~270+ files across core/*, apiserver/*, cmd/*, etc.
- Import test files updated to include new dependencies
- Script patches in `scripts/errors-patch/patches/*.patch`