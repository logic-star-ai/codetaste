# Convert FL to proper D enum

Refactor `FL` from a `ubyte` alias + anonymous enum to a proper D enum with explicit type. Rename all `FLxxx` constants to `FL.xxx` throughout the backend codebase.