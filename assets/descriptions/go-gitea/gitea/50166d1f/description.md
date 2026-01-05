# Penultimate round of `db.DefaultContext` refactor

## Summary

Continue removing direct usage of `db.DefaultContext` by threading `context.Context` through function calls across authentication, models, routers, services, and templates.

## Why

- Enables proper context propagation for cancellation, timeout handling, and request tracing
- Part of broader effort to eliminate global context usage (part of #27065)
- Improves testability and request lifecycle management

## Changes

**Auth Models** (`models/auth/`)
- `Sources()`, `GetSourceByID()`, `CreateSource()`, `UpdateSource()`, `CountSources()`, `ActiveSources()`, `IsSSPIEnabled()` now take `ctx`

**Asymkey Models** (`models/asymkey/`)
- `AddPublicKey()`, `GetPublicKeyByID()`, `SearchPublicKey()`, `ListPublicKeys()`, `UpdatePublicKeyUpdated()`, `PublicKeyIsExternallyManaged()`, `SynchronizePublicKeys()`, `AddPublicKeysBySource()` now take `ctx`
- Deploy key and SSH key verification functions updated

**Issue/Pull Request Models** (`models/issues/`)
- `CreateIssueDependency()`, `RemoveIssueDependency()` now take `ctx`
- `NewIssueLabel()`, `NewIssueLabels()`, `ClearIssueLabels()`, `ReplaceIssueLabels()` now take `ctx`
- `LockIssue()`, `UnlockIssue()` now take `ctx`
- `ChangeProjectAssign()`, `MoveIssueAcrossProjectBoards()` now take `ctx`
- `GetRepoIDsForIssuesOptions()`, `GetMilestones()` now take `ctx`
- PR: `Update()`, `UpdateCols()`, `IsWorkInProgress()`, `Mergeable()`, `GetApprovers()`, `GetBaseBranchLink()`, `GetHeadBranchLink()` now take `ctx`

**Repository Models** (`models/repo/`)
- `GetRepositoryByName()`, `GetRepositoriesMapByIDs()`, `FindReposMapByIDs()` now take `ctx`
- `ComposeMetas()`, `ComposeDocumentMetas()`, `AllowsPulls()`, `RelAvatarLink()`, `TemplateRepo()` now take `ctx`
- `GetTopLanguageStats()`, `UpdateLanguageStats()`, `CopyLanguageStat()` now take `ctx`
- `GetUnindexedRepos()`, `SearchRepositoryIDs()` now take `ctx`

**Admin CLI** (`cmd/`)
- Auth management commands updated to pass context

**Services**
- `UploadAvatar()`, `DeleteAvatar()` now take `ctx`
- `ChangeMilestoneAssign()` now takes `ctx`
- Archive service `Init()` and `ArchiveRepository()` now take `ctx`

**Routers/API**
- Updated to pass context through to model/service calls

**Templates**
- Repository/issue rendering functions now pass `ctx` for meta composition

## Scope

~40 files modified across `cmd/`, `models/`, `routers/`, `services/`, `templates/` with focus on auth sources, SSH keys, issues/PRs, repositories, and user avatars.