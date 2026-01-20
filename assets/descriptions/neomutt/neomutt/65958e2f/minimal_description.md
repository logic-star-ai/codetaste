# Disentangle sort constants - move from centralized to component-specific

Refactor sort methods from a single centralized set of `SORT_*` constants to component-specific enums. Each component (Alias, Browser, Sidebar, Ncrypt, Email) now defines its own sort constants, reducing coupling and dependencies.