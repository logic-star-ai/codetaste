# Refactor ingest CLI to use subcommand architecture

Refactor the ingest CLI from a monolithic command with connector-prefixed options to a subcommand-based architecture where each connector has its own subcommand.