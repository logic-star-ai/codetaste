# Core header refactor: consolidate struct definitions to break cross-header dependencies

Moves most struct definitions from various `pycore_*` headers into two new centralized headers (`pycore_structs.h` and `pycore_runtime_structs.h`) to eliminate circular dependencies.