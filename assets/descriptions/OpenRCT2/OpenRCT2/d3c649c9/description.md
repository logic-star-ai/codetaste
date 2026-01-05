# Rename Peep properties to distinguish Actions from Animations

## Summary
Refactor `Peep` struct and related code to clearly separate **Action** (gameplay state) from **Animation** (sprite rendering) concepts. Rename types, properties, and functions throughout codebase for clarity.

## Why
Current naming conventions for `Peep` properties are confusing:
- `Action` properties (gameplay behavior)
- `ActionSprite` properties (visual representation)
- Both had very similar names, causing confusion

This is a prerequisite for staff costume objects work.

## Changes

### Type Renames
- `PeepActionSpriteType` → `PeepAnimationType`
- `PeepSpriteType` → `PeepAnimationGroup`
- `PeepAnimationGroup` (struct) → `PeepAnimations`

### Peep Struct Properties
- `SpriteType` → `AnimationGroup`
- `ActionSpriteType` → `AnimationType`
- `NextActionSpriteType` → `NextAnimationType`
- `ActionSpriteImageOffset` → `AnimationImageIdOffset`
- `ActionFrame` → `AnimationFrameNum`
- `WalkingFrameNum` → `WalkingAnimationFrameNum`

### Function Renames
- `UpdateCurrentActionSpriteType()` → `UpdateCurrentAnimationType()`
- `SwitchNextActionSpriteType()` → `SwitchNextAnimationType()`
- `GetActionSpriteType()` → `GetAnimationType()`
- `UpdateSpriteType()` → `UpdateAnimationGroup()`
- `SetSpriteType()` → `SetAnimationGroup()`

### Notable Enum Changes
- `PeepActionSpriteType::Ui` → `PeepAnimationType::Hanging`
- `PeepActionSpriteType::StaffCheckboard` → `PeepAnimationType::StaffCheckBoard`

### Other
- Viewport interaction: `SpriteType` → `interactionType`
- `gSpriteTypeToSlowWalkMap` → `gAnimationGroupToSlowWalkMap`
- Animation data constants: `kPeepAnimationGroup*` → `kPeepAnimations*`
- Sprite state IDs: `*Ui*` → `*Hanging*` where appropriate

## Scope
- ~45 files changed
- Guest/Staff entities
- Animation system
- Serialization (park files, save/load)
- RCT1/RCT2 import
- Scripting bindings
- UI windows