# Refactor DBContext to standard Go context.Context

Remove special handling of `DBContext` and make it a standard Go `context.Context`. Replace `db.DefaultContext()` function with `db.DefaultContext` variable and introduce `db.GetEngine(ctx)` helper to retrieve database engine from any context.