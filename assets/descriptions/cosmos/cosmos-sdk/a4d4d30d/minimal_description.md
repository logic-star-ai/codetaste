# Migrate calls from alias file to appropriate store/types

Remove the `types/store.go` alias file and migrate all references to use `store/types` directly. This involves updating imports, type references, and function signatures throughout the codebase to reference store types from their actual location rather than through SDK type aliases.