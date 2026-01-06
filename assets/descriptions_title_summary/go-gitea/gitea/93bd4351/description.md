# Refactor `db.DefaultContext` usage to accept context parameters

Refactor functions across models, services, and routers to accept `context.Context` as a parameter instead of using hardcoded `db.DefaultContext` internally. This enables proper context propagation for cancellation, deadlines, and tracing.