# Refactor: Invert configuration-runtime relationship and eliminate global logger

Major architectural refactoring that inverts the relationship between Configuration and Runtime, eliminates global logger dependencies, and reorganizes code into clearer package boundaries. Runtime now owns Configuration instead of Configuration owning Runtime, and all logging is explicitly dependency-injected.