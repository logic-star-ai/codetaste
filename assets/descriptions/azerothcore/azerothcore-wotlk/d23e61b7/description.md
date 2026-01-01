# Refactor: Centralize World State Definitions

## Summary
Consolidate scattered world state enum definitions from individual script headers into a centralized `WorldStateDefines.h` file with consistent naming conventions.

## Why
- World state enums were scattered across multiple header files (battlegrounds, battlefields, instances, outdoor PvP scripts)
- Inconsistent naming conventions made maintenance difficult
- Hardcoded values mixed with enum definitions
- No single source of truth for world state IDs

## Changes
- [x] Create `WorldStateDefines.h` as central definition file
- [x] Move world state enums from script headers to centralized file
- [x] Standardize naming with clear prefixes:
  - `WORLD_STATE_BATTLEFIELD_*` for battlefields (WG, ...)
  - `WORLD_STATE_BATTLEGROUND_*` for battlegrounds (AB, AV, EY, IC, SA, WS, ...)
  - `WORLD_STATE_ARENA_*` for arenas
  - `WORLD_STATE_OPVP_*` for outdoor PvP zones (EP, HP, NA, SI, TF, ZM, GH)
  - `WORLD_STATE_<INSTANCE>_*` for instance-specific states
  - `WORLD_STATE_CUSTOM_*` for custom/misc states
- [x] Update all references across codebase
- [x] Remove old enum definitions from individual headers
- [x] Add includes for `WorldStateDefines.h` where needed

## Affected Areas
- Battlefields: Wintergrasp
- Battlegrounds: AB, AV, BE, DS, EY, IC, NA, RL, RV, SA, WS
- Arenas: All arena types
- Instances: Black Morass, Halls of Reflection, ICC, Oculus, Ruby Sanctum, Trial of Crusader, Ulduar, Violet Hold, Old Hillsbrad
- Outdoor PvP: EP, HP, NA, SI, TF, ZM, GH
- Core: BattlegroundMgr, Player.cpp
- Scripts: Wintergrasp zone, STV Fishing Extravaganza, ...