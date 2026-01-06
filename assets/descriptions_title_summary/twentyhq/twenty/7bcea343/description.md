# Refactor hotkeys into dedicated lib folder with scoped enums

Refactor hotkey management system by:
- Moving from `@/hotkeys` → `@/lib/hotkeys`
- Breaking down monolithic `InternalHotkeysScope` enum into domain-specific enums
- Removing external dependencies from hotkeys module
- Standardizing naming from plural "hotkeys*" to singular "hotkey*"