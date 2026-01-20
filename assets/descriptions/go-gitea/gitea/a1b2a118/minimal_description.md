# Continue `db.DefaultContext` removal - propagate context to model functions

Refactor model layer functions to accept `context.Context` parameter instead of hardcoding `db.DefaultContext` internally.