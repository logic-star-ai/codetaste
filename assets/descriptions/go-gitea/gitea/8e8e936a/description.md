# Title
-----
Refactor: Move access and repo permission to `models/perm/access`

# Summary
-------
Reorganize access control and repository permission logic by moving it from the root `models` package to a dedicated `models/perm/access` package. Extract collaboration-related code to `models/repo/collaboration.go`.

# Changes
---
**Package Structure:**
- Move `models/access.go` → `models/perm/access/access.go`
- Move `models/repo_permission.go` → `models/perm/access/repo_permission.go`
- Move `models/access_test.go` → `models/perm/access/access_test.go`
- Create `models/repo/collaboration.go` for collaboration logic
- Create `models/repo/collaboration_test.go`

**Code Updates:**
- Export functions: `RecalculateTeamAccesses`, `RecalculateUserAccess`, `RecalculateAccesses`
- Update all imports across codebase to use `access_model "code.gitea.io/gitea/models/perm/access"`
- Move `Collaboration` struct and related methods to `models/repo` package
- Update ~100+ files with new import paths

**Affected Areas:**
- API routes (v1/repo/*, v1/org/team, v1/user/*)
- Web routes (repo/*, user/*)
- Services (pull, issue, automerge, lfs, repository, notification)
- Integration tests
- Private routes (hook_pre_receive, serv)

# Why
---
- Better package organization and separation of concerns
- Clearer ownership of access control logic
- Reduces bloat in root `models` package
- Improves code discoverability and maintainability

# Technical Details
---
- Pure refactoring - no behavioral changes
- All existing tests pass with updated imports
- Function signatures unchanged except for visibility (capitalization)
- Context parameters propagated consistently throughout