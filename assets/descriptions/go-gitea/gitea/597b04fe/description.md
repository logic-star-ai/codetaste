Title
-----
Refactor: Remove `db.DefaultContext` usage across models and services (round 2)

Summary
-------
Continue refactoring to eliminate `db.DefaultContext` usage by adding `context.Context` parameters to functions that previously relied on the global default context.

Why
---
- Enable proper context propagation for cancellation, timeouts, and tracing
- Part of ongoing effort to remove global `db.DefaultContext` (#27065)
- Improve testability and request lifecycle management

Changes
-------
**Models**
- `activities`: `GetUserHeatmapData*` functions now accept context
- `asymkey`: `CountUserGPGKeys`, `GetGPGKey*`, `DeleteGPGKey`, `AddGPGKey`, `RewriteAllPublicKeys`, etc.
- `issues`: `RecalculateIssueIndexForRepo`, `GetIssueStats`, `FindCommentReactions`, `FindIssueReactions`, `Create*Reaction`, `Delete*Reaction`, `GetReviews*`, `CountReviews`
- `organization`: `SearchTeam` accepts context
- `repo`: `GetRelease`, `CountReleasesByRepoID`, `GetLatestReleaseByRepoID`, `PushUpdateDeleteTag`, `SaveOrUpdateTag`, `InsertReleases`, `UpdateReleasesMigrationsByType`
- `system`: `Notices`, `DeleteNotice*`, `DeleteOldSystemNotices`
- `user`: `LookupUserRedirect`

**Services**
- `asymkey`: `DeleteDeployKey`, `DeletePublicKey` accept context
- `auth/source`: LDAP sync operations use provided context
- `externalaccount`: `LinkAccountToUser`, `UpdateMigrationsByType` accept context
- `packages`: All package creation/deletion operations (`CreatePackageAndAddFile`, `RemovePackageVersion`, etc.)
- `release`: `UpdateRelease` accepts context
- `repository`: `CanUserDelete`, `SyncReleasesWithTags` accept context

**Routers & Commands**
- API endpoints updated to pass request context
- Web handlers updated to pass request context
- Admin commands updated to pass context

Impact
------
- Function signatures changed across ~100+ functions
- All callers updated to pass context parameter
- No functional changes, pure refactoring