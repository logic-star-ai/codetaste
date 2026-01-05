# Consolidate hybridcloud modules into canonical location

## Summary
Consolidate `sentry.services.hybrid_cloud` and `sentry.hybridcloud` modules to eliminate redundancy. Choose `sentry.hybridcloud` as canonical module (shorter name, aligns with domain-based structure).

## Background
With most hybridcloud services activity complete, having both `sentry.services.hybrid_cloud` and `sentry.hybridcloud` creates unnecessary confusion and duplication.

## Changes

### Module Migrations
- `sentry.services.hybrid_cloud.pagination` → `sentry.hybridcloud.rpc.pagination`
- `sentry.services.hybrid_cloud.sig` → `sentry.hybridcloud.rpc.sig`
- `sentry.services.hybrid_cloud.region` → `sentry.hybridcloud.rpc.resolvers`
- `sentry.services.hybrid_cloud.filter_query` → `sentry.hybridcloud.rpc.filter_query`
- `sentry.hybridcloud.rpc.services.caching` → `sentry.hybridcloud.rpc.caching`
- `sentry.services.hybrid_cloud.util.{region,control,all}_silo_function` → `sentry.silo.base`
- `sentry.services.hybrid_cloud.util.flags_to_bits` → `sentry.services.hybrid_cloud.organization.model`

### Updates
- Import statements updated across ~60+ files (API endpoints, integrations, services, models, tests...)
- Compatibility shims added for backward compatibility with getsentry
- Cleaned up `__init__.py` files to use explicit exports vs `import *`

### Files Affected
- API endpoints (`group_integrations.py`, `seer_rpc.py`, ...)
- Integrations (GitHub, GitLab, MSTeams, VSTS, AWS Lambda, Jira, PagerDuty, ...)
- Services (app, organization, project, user, integration, ...)
- Models (`User`, `SentryAppInstallation`)
- Tests, migrations, middleware, notifications, receivers, ...

## Scope
This is **part 1** of consolidation. Additional RPC supporting code will be moved in subsequent PRs to keep changes reviewable.