# Move RpcModel and utilities to sentry.hybridcloud.rpc

## Summary
Move `RpcModel`, delegation classes (`DelegatedBySiloMode`, `DelegatedByOpenTransaction`), utility functions (`coerce_id_from`, `extract_id_from`, ...), constants (`IDEMPOTENCY_KEY_LENGTH`, `REGION_NAME_LENGTH`, ...), and related infrastructure from `sentry.services.hybrid_cloud` to `sentry.hybridcloud.rpc`.

## Why
Consolidating the two hybridcloud modules together to improve organization and reduce module fragmentation. The RPC infrastructure belongs in `sentry.hybridcloud.rpc` rather than `sentry.services.hybrid_cloud`.

## Changes
- Move ~250 lines of code from `src/sentry/services/hybrid_cloud/__init__.py` to `src/sentry/hybridcloud/rpc/__init__.py`
- Update all imports across the codebase:
  - API endpoints (organization_details, organization_index, ...)
  - Models (organizationmapping, organizationmember, outbox, ...)
  - Services (access, auth, organization, project, ...)
  - RPC infrastructure (filter_query, pagination, resolvers, service, sig)
  - Various other modules (integrations, issues, notifications, ...)
- Create temporary shim in `sentry.services.hybrid_cloud.__init__.py` that re-exports `RpcModel` and `coerce_id_from` for backward compatibility
- Add TODO comment indicating shim removal pending getsentry update

## Scope
- ~40 files updated with import path changes
- No functional changes—pure refactoring
- Maintains backward compatibility via shim module