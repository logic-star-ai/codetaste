# Consolidate integration models to `sentry/integrations/models` directory

Move all integration-related models from `sentry/models/integrations/` to `sentry/integrations/models/` and update corresponding tests to `tests/sentry/integrations/models/`. Update all imports across the codebase to reflect new paths.