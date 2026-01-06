# Refactor `db.DefaultContext` usage in template-accessible functions

Refactor functions used in templates to accept `context.Context` as parameter instead of implicitly using `db.DefaultContext`.