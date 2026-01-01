# Refactor game states into Scene architecture

## Summary
Introduce `Scene` abstraction to replace fragmented game state logic. Implements `IntroScene`, `TitleScene`, and `GameScene` as concrete scene types, managed through `Context`.

## Why
- Current architecture uses scattered global state (`gIntroState`, `gScreenFlags`) and direct function calls (`IntroUpdate()`, `TitleLoad()`)
- No clear separation between different game states (intro, title, gameplay)
- Difficult to extend with new states (editor, loading screen)
- Scene pattern provides clean abstraction for state transitions and lifecycle management

## Changes

### Core Architecture
- Add `IScene` interface with `Load()`, `Tick()`, `Stop()` methods
- Add base `Scene` class with context/game state access
- Replace main loop logic: `IntroUpdate()` / `TitleScreen::Tick()` / `gameStateTick()` → `activeScene->Tick()`

### Scene Implementations
- `IntroScene` - encapsulates intro sequence (publisher/developer logos, fade effects)
  - Moves logic from `Intro.cpp`
  - Removes global `gIntroState`, managed internally
  - Transitions to `TitleScene` on completion
- `TitleScene` - handles title screen and title sequences
  - Moves from `title/TitleScreen.*` → `scenes/title/TitleScene.*`
  - Manages title sequence player, preview mode
- `GameScene` - wraps actual gameplay
  - Calls `gameStateTick()`
  - Sets `SCREEN_FLAGS_PLAYING`
  - Stops audio on scene exit

### Context Integration
- Add scene getters: `Get{Loading,Intro,Title,Game,Editor}Scene()`
- Add `GetActiveScene()` / `SetActiveScene(IScene*)`
- `SetActiveScene()` calls `Stop()` on old scene, `Load()` on new scene
- Initialize all scenes in constructor

### Cleanup
- Replace `TitleLoad()` calls → `SetActiveScene(GetTitleScene())`
- Replace `gIntroState` checks → `IntroIsPlaying()`
- Remove intro state checks from UI windows (TitleExit, TitleOptions)
- Move `title/*` → `scenes/title/*` (including Command/*, TitleSequence*, etc.)
- Update includes across codebase

## Implementation Details
- Scene lifecycle: `Load()` → repeated `Tick()` → `Stop()`
- Scenes access context via `GetContext()`, game state via `GetGameState()`
- Intro scene uses static state internally (temporary, encapsulated)
- Title scene wraps existing `ITitleSequencePlayer` logic
- Game scene minimal wrapper around `gameStateTick()` for now

## Future Work (not in scope)
- `EditorScene` for scenario editor
- `LoadingScene` for preload phase
- Further refactoring of scene-specific logic