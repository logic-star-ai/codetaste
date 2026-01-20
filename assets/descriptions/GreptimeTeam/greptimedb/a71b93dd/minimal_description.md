# Refactor: Remove cluster_id field from codebase

Remove unused `cluster_id` field throughout the codebase. The field was originally intended to isolate nodes from different clusters (allowing metasrv to be shared among various GreptimeDB clusters), but is not assigned anywhere and is largely ignored, causing confusion.