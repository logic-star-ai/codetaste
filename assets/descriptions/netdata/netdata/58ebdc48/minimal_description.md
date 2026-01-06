# Rename `appconfig` to `inicfg` and remove `config_*` convenience macros

Refactor configuration subsystem by renaming `appconfig` → `inicfg` and removing function-like macros that implicitly referenced `netdata_config`.