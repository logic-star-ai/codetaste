# Refactor template functions to accept explicit context parameter

Remove `db.DefaultContext` usage from functions called in templates. These functions now require an explicit `context.Context` parameter instead of using the default context internally.