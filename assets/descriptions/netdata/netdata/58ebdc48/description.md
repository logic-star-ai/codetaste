# Rename `appconfig` to `inicfg` and remove `config_*` convenience macros

## Summary
Refactor configuration subsystem by renaming `appconfig` → `inicfg` and removing function-like macros that implicitly referenced `netdata_config`.

## Changes

### Renaming
- `appconfig*` → `inicfg*` (all functions, types, files)
- `src/libnetdata/config/appconfig*` → `src/libnetdata/inicfg/inicfg*`
- `APPCONFIG_*` → `INICFG_*` (constants/macros)

### Macro Removal
Replace convenience macros with explicit function calls:
- `config_get(...)` → `inicfg_get(&netdata_config, ...)`
- `config_set(...)` → `inicfg_set(&netdata_config, ...)`
- `config_get_boolean(...)` → `inicfg_get_boolean(&netdata_config, ...)`
- `config_get_number(...)` → `inicfg_get_number(&netdata_config, ...)`
- `config_get_duration_*(...)` → `inicfg_get_duration_*(&netdata_config, ...)`
- `config_get_size_*(...)` → `inicfg_get_size_*(&netdata_config, ...)`
- ...and all other variants

### API Consolidation
Merge separate API files into single `inicfg_api.c`:
- `appconfig_api_text.{c,h}` (deleted)
- `appconfig_api_numbers.{c,h}` (deleted)
- `appconfig_api_boolean.{c,h}` (deleted)
- `appconfig_api_sizes.{c,h}` (deleted)
- `appconfig_api_durations.{c,h}` (deleted)
→ `inicfg_api.c` (consolidated)

### File Structure
- `src/libnetdata/config/` → `src/libnetdata/inicfg/`
- New `config/config.h` wrapper includes `inicfg/*.h`
- `dyncfg.{c,h}` moved to `inicfg/` directory

### Call Sites
Update ~1000+ call sites across:
- collectors (cgroups, diskspace, ebpf, freebsd, macos, proc, etc.)
- streaming subsystem
- web server
- claim/cloud configuration
- ML configuration
- registry
- socket listeners
- ...all modules using configuration

## Why
- Clearer naming: "inicfg" = INI configuration
- Explicit config root parameter improves code clarity
- Reduced macro indirection
- Easier to work with multiple config instances
- Better code maintainability

## Testing
- CI jobs (existing tests should pass)
- No functional behavior changes expected