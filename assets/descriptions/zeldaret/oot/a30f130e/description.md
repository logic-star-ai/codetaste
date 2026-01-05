# Target → Attention (System Rename)

## Summary
Rename the "Target" system to "Attention" system throughout the codebase to better reflect its actual purpose and align with naming conventions from GameCube Zelda titles.

## Why
The system currently named "Target" creates confusion because:
- "Z Target" is overloaded and doesn't match implementation
- The system doesn't handle actual lock-on (that's `player->focusActor` + camera)
- It only brings actors to player's attention via Navi, arrows, reticles, and enemy BGM
- Original GameCube Zelda symbols use "Attention" naming (e.g., `dAttention_c::GetLockonList`)

## Changes

### Core System
- `TargetContext` → `Attention`
- `targetCtx` → `attention`
- `Target_*()` functions → `Attention_*()`
- `FindTargetableActor()` → `FindActor()`

### Actor Fields
- `targetMode` → `attentionRangeType` (with comment explaining attention/leash ranges)
- `targetArrowOffset` → `lockOnArrowOffset`
- `targetPriority` → `attentionPriority`
- `targetableActorP` → `attentionActorP`

### Enums & Data
- `TargetMode` → `AttentionRangeType`
- `TARGET_MODE_*` → `ATTENTION_RANGE_*` (with range comments)
- `TargetColor` → `AttentionColor` (primary/secondary fields)
- `sTargetRanges[]` → `sAttentionRanges[]` (with attention/leash range docs)

### Assets
- `gZTargetArrowDL` → `gLockOnArrowDL`
- `gZTargetLockOnTriangleDL` → `gLockOnReticleTriangleDL`

### Documentation
Add comprehensive system description explaining:
- Navi hover behavior
- Arrow/reticle display
- Enemy BGM triggering
- Separation from actual lock-on implementation