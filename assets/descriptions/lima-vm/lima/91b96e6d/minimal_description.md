# Refactor: Extract common types and functions to `pkg/limatype`

Refactor code organization by creating a new `pkg/limatype` package to hold common types, constants, and utility functions previously scattered across `pkg/limayaml` and `pkg/store`. Update all imports throughout the codebase to use the new package structure.