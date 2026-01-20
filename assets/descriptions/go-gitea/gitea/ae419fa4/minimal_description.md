# Final round of `db.DefaultContext` refactor

Complete the removal of hardcoded `db.DefaultContext` usage throughout the codebase by propagating `context.Context` properly through all layers (models, services, routers, modules).