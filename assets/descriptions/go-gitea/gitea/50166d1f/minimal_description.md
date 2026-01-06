# Penultimate round of `db.DefaultContext` refactor

Continue removing direct usage of `db.DefaultContext` by threading `context.Context` through function calls across authentication, models, routers, services, and templates.