# Refactor: Move plugin hook methods to `plugin.hooks.*` namespace

Reorganize plugin hook methods (`fireHook`, `registerHook`, `hasListeners`, `unregisterHook`) into dedicated `plugins.hooks.*` namespace for better code organization and separation of concerns.