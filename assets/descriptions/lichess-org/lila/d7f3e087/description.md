# Title

Refactor code organization for improved code splitting

## Summary

Major refactoring to improve code organization and enable better code splitting by:
- Moving shared utilities from `site` to `common` module
- Consolidating scattered `userComplete` functionality into single location
- Reducing reliance on global `site` object
- Making dependencies explicit through direct imports

## Changes

### Module Relocations

- `site/log.ts` → `common/dbLog.ts`
- `site/watchers.ts` → `common/watchers.ts`
- `site/clockWidget.ts` → `common/clock.ts` (as `setClockWidget`)
- `site/timeago.ts` → `common/i18n.ts` + `site/renderTimeAgo.ts`
- `bits/userComplete.ts` → `common/userComplete.ts`
- `bits/css/_complete.scss` → `common/css/component/_complete.scss`

### Consolidated Mini Game/Board

- Merged `site/miniGame.ts` functionality into `common/miniBoard.ts`
- Exports: `initMiniGame`, `initMiniGames`, `updateMiniGame`, `finishMiniGame`
- All modules now import directly instead of via `site.miniGame.*`

### Global Site Object Cleanup

Removed from global `site`:
- `clockWidget` → import `setClockWidget` from `common/clock`
- `spinnerHtml` → import from `common/spinner`
- `makeChat` → import from `chat` module
- `makeChessground` → import `Chessground` from `chessground`
- `userComplete` → import from `common/userComplete`
- `miniBoard.*` / `miniGame.*` → import from `common/miniBoard`
- `timeago` / `dateFormat` → import from `common/i18n`
- `watchers` → import from `common/watchers`
- `log` → import from `common/dbLog`
- `contentLoaded()` → `site.pubsub.emit('content-loaded', ...)`

### Chat Module Changes

- `chat` package now exports `makeChat` directly
- Changed from `site.makeChat(opts)` to `import { makeChat } from 'chat'`
- No longer returns Promise, returns `ChatCtrl` directly

### Type Definition Updates

- Moved `LichessEditor`, `Config`, `Options`, etc. to `editor/src/interfaces.ts`
- Removed `UserCompleteOpts`, `LichessLog`, `MiniGameUpdateData` from global types
- Added `$as` helper to `common` module

## Benefits

- Better module boundaries and dependency management
- Explicit imports instead of global access patterns
- Improved tree-shaking and code splitting capabilities
- Reduced circular dependencies
- Clearer separation between site initialization and common utilities

## Migration Notes

Modules importing affected functionality need to update:
- `site.makeChat(...)` → `makeChat(...)`
- `site.asset.userComplete(...)` → `userComplete(...)`
- `site.makeChessground(...)` → `makeChessground(...)` 
- `site.miniGame.*` / `site.miniBoard.*` → import from `common/miniBoard`
- `site.contentLoaded(el)` → `site.pubsub.emit('content-loaded', el)`
- `site.timeago(...)` → `timeago(...)` from `common/i18n`
- `site.log(...)` → `log(...)` from `common/dbLog`