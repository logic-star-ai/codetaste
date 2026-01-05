Title
-----
Migrate store methods to use `request.Context` instead of `context.Context`

Summary
-------
Refactor store layer and related application methods to consistently use `request.Context` instead of `context.Context`, enabling better request tracking, logging, and context propagation throughout the application.

Why
---
- Pushes `request.Context` as the ubiquitously available context type across the codebase
- Enables consistent context propagation from API handlers through app layer to store layer
- Improves logging and tracing capabilities by maintaining request context
- Reduces reliance on `context.Background()` in favor of proper context passing

Changes
-------

**Store Layer:**
- Update store interface methods to accept `request.CTX` or `*request.Context`:
  - `SessionStore.Get()`, `SessionStore.Save()`, `SessionStore.GetSessions()`
  - `TeamStore.GetMember()`, `TeamStore.GetTeamsForUser()`
  - `EmojiStore.Get()`, `EmojiStore.GetByName()`, `EmojiStore.GetMultipleByName()`
  - `LicenseStore.Get()`
  - `ComplianceStore.MessageExport()`
  - `UploadSessionStore.Get()`
  - `ChannelStore.CreateInitialSidebarCategories()`

**App Layer:**
- Update method signatures to accept and propagate `*request.Context`:
  - Session management: `CreateSession()`, `GetSession()`, `GetSessions()`, `RevokeSession()`, `RevokeSessionById()`, `RevokeAllSessions()`, `RevokeSessionsForDeviceId()`
  - User access tokens: `RevokeUserAccessToken()`, `DisableUserAccessToken()`, `EnableUserAccessToken()`
  - OAuth: `AllowOAuthAppAccessToUser()`, `GetOAuthAccessTokenForCodeFlow()`, `GetOAuthAccessTokenForImplicitFlow()`, `GetOAuthImplicitRedirect()`, `DeauthorizeOAuthAppForUser()`, `RevokeAccessToken()`, `SwitchOAuthToEmail()`
  - Team members: `GetTeamMember()`, `GetTeamMembersForUser()`, `UpdateTeamMemberRoles()`, `UpdateTeamMemberSchemeRoles()`
  - User management: `UpdateActive()`, `UpdateUserActive()`, `DemoteUserToGuest()`, `UserCanSeeOtherUser()`, `FilterUsersByVisible()`, `GetViewUsersRestrictions()`, `RestrictUsersGetByPermissions()`, `RestrictUsersSearchByPermissions()`
  - Permissions: `HasPermissionToTeam()`, `HasPermissionToChannelByPost()`
  - Commands: `ExecuteCommand()`
  - Bots: `UpdateBotActive()`

**Test Updates:**
- Update test helpers to create and use `request.TestContext(t)`
- Replace `context.Background()` calls with proper context passing
- Update mock expectations to include context parameters

**Platform Layer:**
- Update `PlatformService` session methods to use `*request.Context`
- Update WebHub and WebConn to propagate context properly

Implementation Notes
-------------------
- Some methods create `request.EmptyContext()` temporarily where context is not yet available
- Store methods use `c.Context()` to access underlying `context.Context` when needed
- Test context helper signature changed: `TestContext(t testing.TB)` for broader test compatibility
- Generated files (opentracing, retry layer, timer layer, mocks) automatically updated