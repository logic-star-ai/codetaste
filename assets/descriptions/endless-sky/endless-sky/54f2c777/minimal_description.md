# Store pointer to player's ConditionsStore in all ConditionSets to eliminate PlayerInfo passing

Refactor `ConditionSet` and `ConditionAssignments` to store a pointer to the player's `ConditionsStore`, eliminating the need to pass `PlayerInfo` throughout the codebase solely for condition evaluation.