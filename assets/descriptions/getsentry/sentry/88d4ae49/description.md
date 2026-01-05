# Title
-------
Refactor: Relocate organization and project RPC services to domain-specific modules

# Summary
---------
Move organization and project related RPC services from `sentry.services.hybrid_cloud` into dedicated domain modules under `sentry.organizations.services` and `sentry.projects.services`.

# Why
-----
- Integrate RPC services with the rest of application code rather than isolating them
- Remove dependency on the generic `sentry.services.hybrid_cloud` structure
- Enable consolidation of organization/project-related code currently scattered across the codebase
- Improve code organization by grouping services with their domain models

# Changes
---------
**New module structure:**
- `sentry.organizations.services.organization.*` (impl, model, serial, service)
- `sentry.organizations.services.organization_actions.*`
- `sentry.projects.services.project.*`
- `sentry.projects.services.project_key.*`

**Migration:**
- Move all organization service files from `sentry.services.hybrid_cloud.organization`
- Move all project service files from `sentry.services.hybrid_cloud.project`
- Update ~200+ import statements across the codebase
- Maintain backward compatibility with re-exports in old locations (marked with TODO for removal)
- Update RPC service discovery to scan new module paths

**No functional changes** - pure code reorganization

# Refs
------
HC-982