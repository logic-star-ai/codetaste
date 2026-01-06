# Convert entire CLI from Cobra to clibase

Replaced `spf13/cobra` with custom `clibase` framework across all CLI commands, subcommands, and tests. Removed `cliflag` package and migrated all flag/option handling to `clibase.OptionSet`.