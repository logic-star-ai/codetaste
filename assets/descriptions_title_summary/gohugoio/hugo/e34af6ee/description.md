# Refactor to eliminate global state (Viper, i18n, etc.)

Remove all global state from Hugo by eliminating global Viper configuration access and global i18n translator. Replace with explicit dependency injection pattern passing configuration and translation providers through the dependency graph.