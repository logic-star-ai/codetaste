# Refactor: Relocate organization and project RPC services to domain-specific modules

Move organization and project related RPC services from `sentry.services.hybrid_cloud` into dedicated domain modules under `sentry.organizations.services` and `sentry.projects.services`.