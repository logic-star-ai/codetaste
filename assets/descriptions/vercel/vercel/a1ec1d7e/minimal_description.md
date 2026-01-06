# Refactor: Decouple `Output` from `Client` for improved testability

Refactor the `Output` class usage to be a managed singleton instead of being directly coupled to the `Client` instance. This enables better testability of the CLI entrypoint and allows the output configuration to be modified as the program flows.