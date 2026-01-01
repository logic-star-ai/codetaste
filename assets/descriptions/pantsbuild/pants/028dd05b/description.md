# Refactor: Split environments.py into separate subsystem and target_types modules

## Summary

Extract environments-related subsystem and target types from `src/python/pants/core/util_rules/environments.py` into separate modules to resolve import cycle preventing call-by-name syntax migration.

## Why

- Import cycle exists between `core/util_rules/environments.py` and `engine/internals/platform_rules.py` over `DockerImageField` and related classes
- Current structure violates Pants conventions by mixing subsystem, target types, and rules in single file
- Prevents migration to call-by-name syntax in `engine/internals/build_files.py`

## Changes

Create new module structure:
- `src/python/pants/core/environments/subsystems.py` → `EnvironmentsSubsystem`
- `src/python/pants/core/environments/target_types.py` → All environment target types:
  - `LocalEnvironmentTarget`, `LocalWorkspaceEnvironmentTarget`
  - `DockerEnvironmentTarget`, `RemoteEnvironmentTarget`
  - Related field classes: `EnvironmentField`, `DockerImageField`, `DockerPlatformField`, ...
  - `EnvironmentTarget` dataclass
- Rules remain in `src/python/pants/core/util_rules/environments.py`

Update ~40 import sites across codebase to reflect new locations.