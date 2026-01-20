# Remove `errs.Must` from service packages to prevent runtime panics

Replace all uses of `errs.Must()` within `internal/service/**/` with explicit error handling to avoid crashing the provider during resource operations.