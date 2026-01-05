Title
-----
Complete `RpcActor` → `Actor` rename and remove compatibility shim

Summary
-------
Complete the actor type rename throughout the codebase by updating all import paths and references from `RpcActor` to `Actor`, and remove the compatibility shim module.

Why
---
The actor type was previously renamed from `RpcActor` to `Actor`, but a compatibility shim was maintained at `sentry.services.hybrid_cloud.actor` for backward compatibility. This tech debt needs to be cleaned up.

Changes
-------
- Remove shim module at `src/sentry/services/hybrid_cloud/actor.py`
- Update all imports from `sentry.services.hybrid_cloud.actor.RpcActor` → `sentry.types.actor.Actor`
- Update all `RpcActor` references in code to use `Actor`
- Update type hints: `RpcActor` → `Actor` throughout
- Move test file: `tests/sentry/hybridcloud/test_actor.py` → `tests/sentry/types/test_actor.py`

Scope
-----
Affects ~100+ files across:
- API endpoints & serializers
- Notification system
- Issue assignment & ownership
- Alert rules & monitors
- Integrations (Slack, MSTeams, Discord)
- Digest utilities
- Test suites