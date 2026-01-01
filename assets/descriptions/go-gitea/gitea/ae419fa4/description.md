Title
-----
Final round of `db.DefaultContext` refactor

Summary
-------
Complete the removal of hardcoded `db.DefaultContext` usage throughout the codebase by propagating `context.Context` properly through all layers (models, services, routers, modules).

Why
---
- Improves context handling and cancellation propagation
- Enables proper tracing and request-scoped data flow
- Eliminates technical debt from hardcoded context usage
- Allows for better control over database operations lifecycle

Changes
-------

**Models Layer (`models/...`)**
- `asymkey`: Add `ctx` parameter to `GPGKeyToEntity`, `GetGPGImportByKeyID`, `VerifyGPGKey`, `VerifySSHKey`, `HasDeployKey`, `AddDeployKey`, `UpdateDeployKeyCols`, `CountDeployKeys`, `AddPrincipalKey`, `ListPrincipalKeys`
- `auth`: Add `ctx` to `OAuth2Application.GenerateClientSecret`, `UpdateOAuth2Application`, `DeleteOAuth2Application`, `ListOAuth2Applications`, `GetActiveOAuth2ProviderSources`, `GetActiveOAuth2SourceByName`
- `avatars`: Add `ctx` to `GetEmailForHash`, `saveEmailHash` (internal)
- `repo`: Add `ctx` to `LookupRedirect`
- `user`: Add `ctx` to `GetExternalLogin`, `ListAccountLinks`, `LinkExternalToUser`, `RemoveAccountLink`, `GetUserIDByExternalUserID`, `UpdateExternalUserByExternalID`, `FindExternalUsersByProvider`
- `webhook`: Add `ctx` to `HookTasks`, `UpdateHookTask`, `Webhook.History`, `getWebhook`, `Get*ByID/ByRepoID/ByOwnerID`, `CountWebhooksByOpts`, `Update*`, `Delete*`

**Services Layer (`services/...`)**
- `auth/source`: `DeleteSource` → add `ctx` parameter
- `auth/source/oauth2`: `Init`, `ResetOAuth2`, `GetActiveOAuth2Providers` → add `ctx`
- `externalaccount`: Update `LinkAccountToUser`, `UpdateExternalUser` to use passed context
- `migrations`: Update external user remapping to pass context
- `pull`: `MergedManually`, `getAllCommitStatus` → add `ctx`
- `webhook/deliver`: Use passed context instead of `db.DefaultContext`
- `convert`: `ToStopWatches` → add `ctx` for issue/repo lookups

**Routers/Handlers (`routers/...`)**
- `cmd/admin_auth.go`: Pass `ctx` to `DeleteSource`
- API endpoints: Pass request context to model/service functions
- Web handlers: Pass handler context to model/service functions
- Update `Repository.CanUseTimetracker`, `Repository.CanCreateIssueDependencies` → add `ctx`

**Modules (`modules/...`)**
- `context/repo.go`: Update helper methods to accept context
- `eventsource/manager_run.go`: Pass context to `ToStopWatches`

**Initialization (`routers/init.go`)**
- Update `oauth2.Init` call to pass context

**Tests**
- Update all test files to use `db.DefaultContext` explicitly where needed
- Update assertions and setup code

Implementation Notes
-------------------
- Replace all `db.GetEngine(db.DefaultContext)` → `db.GetEngine(ctx)`
- Replace all `db.TxContext(db.DefaultContext)` → `db.TxContext(ctx)`
- Chain context through call stacks from HTTP handlers down to DB operations
- Maintain backward compatibility in tests by passing `db.DefaultContext` explicitly