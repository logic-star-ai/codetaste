# Title

Store pointer to player's ConditionsStore in all ConditionSets to eliminate PlayerInfo passing

# Summary

Refactor `ConditionSet` and `ConditionAssignments` to store a pointer to the player's `ConditionsStore`, eliminating the need to pass `PlayerInfo` throughout the codebase solely for condition evaluation.

# Why

Passing `PlayerInfo` around is cumbersome when the vast majority of cases only need access to the player's `ConditionsStore` for evaluating `ConditionSet`s. This creates unnecessary coupling and verbose function signatures.

# What Changed

## ConditionSet & ConditionAssignments
- Added `const ConditionsStore *conditions` member
- Updated constructors/`Load()` to accept `const ConditionsStore *` parameter
- `Test()` and `Evaluate()` no longer require passing conditions as parameters
- `Apply()` now operates on stored pointer instead of requiring parameter

## Load Methods
- All `Load()` methods accepting `ConditionSet`/`ConditionAssignments` now take `const ConditionsStore *playerConditions`
- Propagated through: `Mission`, `Conversation`, `GameEvent`, `GameAction`, `NPC`, `Planet`, `System`, `News`, `StartConditions`, `TextReplacements`, etc.

## Function Signatures Simplified
- `Mission::IsFailed()` no longer needs `PlayerInfo` parameter
- `CargoHold::IllegalCargoFine()` / `IllegalPassengersFine()` no longer need `PlayerInfo`
- `Conversation::HasAnyChoices()` / `ShouldDisplayNode()` simplified
- ... and many others

## Initialization Order
- `PlayerInfo` now created before `GameData::BeginLoad()`
- Passed to `UniverseObjects::Load()` → `LoadFile()` to populate condition pointers during loading

# Impact

Function calls throughout engine now cleaner where conditions are evaluated without dragging `PlayerInfo` references through call chains.