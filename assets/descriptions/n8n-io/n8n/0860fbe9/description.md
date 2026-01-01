# Refactor: Rename task runner files and classes for clarity

## Summary

Rename several task runner files, directories, and classes to improve clarity and consistency across the codebase.

## Changes

### Directory Structure
- `runners/` → `task-runners/`

### Files
- `runner-types.ts` → `task-runner-types.ts`
- `runner-ws-server.ts` → `task-runner-ws-server.ts`
- `runner-lifecycle-events.ts` → `task-runner-lifecycle-events.ts`
- `task-manager.ts` → `task-requester.ts`
- `local-task-manager.ts` → `local-task-requester.ts`

### Classes
- `TaskManager` → `TaskRequester`
- `LocalTaskManager` → `LocalTaskRequester`
- `RunnerLifecycleEvents` → `TaskRunnerLifecycleEvents`

### Methods
- `startAgentJob()` → `startRunnerTask()`

## Why

- Better reflects the actual role of classes (e.g., `TaskRequester` more accurately describes its purpose than `TaskManager`)
- Consistent naming with `task-runner` prefix throughout the module
- Improves code readability and maintainability
- Clearer separation between task runners and other execution concepts

## Scope

- Import path updates across CLI and core packages
- Variable/parameter renames for consistency
- Test file relocations
- No functional changes