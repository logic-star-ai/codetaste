# Refactor: Extract Common Utilities to Shared Package

## Summary
Extracts common utility functions from `backend` and `frontend` into a new shared package `@monkeytype/util`. Also creates `@monkeytype/esbuild` package for shared build configuration.

## Why
- Eliminates code duplication between backend and frontend
- Centralizes utility functions for better maintainability
- Provides single source of truth for common operations
- Improves code reusability across the monorepo

## Changes

### New Packages Created
- `@monkeytype/util` - Shared utility functions
  - `arrays.ts` - Array operations (intersect)
  - `date-and-time.ts` - Timestamp/date utilities (getCurrentDayTimestamp, getStartOfDayTimestamp, isToday, isYesterday, getStartOfWeekTimestamp, getCurrentWeekTimestamp, constants)
  - `numbers.ts` - Number utilities (roundTo1, roundTo2, stdDev, mean, median, kogasa, randomIntFromRange, mapRange)

- `@monkeytype/esbuild` - Shared esbuild configuration

### Migrations
- Backend: Updated imports to use `@monkeytype/util/*` instead of local utils
- Frontend: Updated imports to use `@monkeytype/util/*` instead of local utils
- Moved tests from `backend/__tests__/utils/misc.spec.ts` to `packages/util/__test__/*.spec.ts`
- Removed duplicate function implementations from backend/frontend utils

### Updated Files
- `backend/src/utils/misc.ts` - Removed functions now in shared package
- `frontend/src/ts/utils/...` - Removed duplicate implementations
- All consumers updated to import from `@monkeytype/util/*`