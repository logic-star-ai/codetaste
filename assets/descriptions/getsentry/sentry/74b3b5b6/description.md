# Title

Consolidate integration models to `sentry/integrations/models` directory

# Summary

Move all integration-related models from `sentry/models/integrations/` to `sentry/integrations/models/` and update corresponding tests to `tests/sentry/integrations/models/`. Update all imports across the codebase to reflect new paths.

# Why

- Better code organization by co-locating integration models with integration logic
- Improves discoverability of integration-related code
- Aligns with control silo architecture patterns
- Reduces split between models and integration implementations

# What

## Models to Move

- `Integration` → `sentry/integrations/models/integration.py`
- `OrganizationIntegration` → `sentry/integrations/models/organization_integration.py`
- `ExternalIssue` → `sentry/integrations/models/external_issue.py`
- `ExternalActor` → `sentry/integrations/models/external_actor.py`
- `DocIntegration` → `sentry/integrations/models/doc_integration.py`
- `DocIntegrationAvatar` → `sentry/integrations/models/doc_integration_avatar.py`
- `IntegrationFeature` → `sentry/integrations/models/integration_feature.py`
- `IntegrationExternalProject` → `sentry/integrations/models/integration_external_project.py`
- `RepositoryProjectPathConfig` → `sentry/integrations/models/repository_project_path_config.py`
- `ProjectIntegration` → `sentry/integrations/models/project_integration.py`

## Tests to Move

- `tests/sentry/models/test_external_actor.py` → `tests/sentry/integrations/models/test_external_actor.py`
- `tests/sentry/models/test_integrationfeature.py` → `tests/sentry/integrations/models/test_integrationfeature.py`
- `tests/sentry/deletions/test_organizationintegration.py` → `tests/sentry/integrations/models/deletions/test_organizationintegration.py`

## Import Updates

Update ~200+ imports across:
- API endpoints
- Serializers
- Integration implementations (GitHub, GitLab, Jira, Slack, etc.)
- Tasks
- Middleware
- Tests
- Fixtures

## Configuration Updates

- Remove `sentry.models.integrations.external_issue` from `pyproject.toml` module exclusions
- Add `__init__.py` with proper `__all__` exports in `sentry/integrations/models/`

# Related

ref #73859 (control silo consolidation)