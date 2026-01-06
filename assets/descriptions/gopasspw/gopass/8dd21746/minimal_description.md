# Refactor command setup

Refactor gopass subcommand configuration to simplify future changes to command structure. Move command definitions from centralized location into module-specific `GetCommands()` functions.