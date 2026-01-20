# Refactor `tbot` CLI architecture for better maintainability and extensibility

Refactor the `tbot` CLI to eliminate the global `CLIConf` namespace, improve code organization, and expose new subcommands for various tbot output types and services through pure CLI (not just config files).