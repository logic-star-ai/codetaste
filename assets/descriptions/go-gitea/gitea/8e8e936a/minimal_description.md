# Refactor: Move access and repo permission to `models/perm/access`

Reorganize access control and repository permission logic by moving it from the root `models` package to a dedicated `models/perm/access` package. Extract collaboration-related code to `models/repo/collaboration.go`.