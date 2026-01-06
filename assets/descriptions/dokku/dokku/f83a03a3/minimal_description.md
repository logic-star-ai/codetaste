# Consolidate Golang Plugin Binaries to Reduce Build Time and Package Size

Refactor compiled golang plugins to use 3 distinct binaries instead of compiling individual binaries for each subcommand and trigger. Use symlinks to route to appropriate entrypoints.