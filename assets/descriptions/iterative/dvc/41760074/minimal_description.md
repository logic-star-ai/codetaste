# Rename `odb` to `cache` throughout codebase

Rename `repo.odb` → `repo.cache` throughout the codebase to clarify terminology and better distinguish between three types of object databases: generic odb (e.g., in-memory), cache (typically local), and remote (typically cloud).