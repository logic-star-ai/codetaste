# Remove circular dependency between Env and PushContext

Refactor `PushContext` to eliminate circular dependency with `Environment`. `PushContext` now directly contains mesh config, networks config, and service/config store interfaces instead of referencing `Environment`.