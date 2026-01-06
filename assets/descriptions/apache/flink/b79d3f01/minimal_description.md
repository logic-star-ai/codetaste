# Refactor deprecated Configuration getter/setter methods to use generic `get()` and `set()`

Replace all usages of deprecated type-specific Configuration methods (`getXxx(ConfigOption<Xxx>)`, `getXxx(ConfigOption<Xxx>, Xxx)`, and `setXxx(ConfigOption<Xxx>, Xxx)`) with the generic `get()` and `set()` methods throughout the codebase.