# Consolidate @calcom/core into @calcom/lib

## Summary

Merge `@calcom/core` package into `@calcom/lib` to eliminate redundant package structure. Both packages contained helper functions and utilities, causing unnecessary separation and dependency complexity.

## Changes

- Delete `packages/core/` directory entirely
- Move all core functionality to `packages/lib/`:
  - `CalendarManager.ts` & tests
  - `EventManager.ts`
  - `videoClient.ts`
  - `getUserAvailability.ts`
  - `getAggregatedAvailability.ts`
  - `getBusyTimes.ts`
  - `event.ts` utilities
  - `location.ts` types
  - `crmManager/` directory
  - `builders/CalendarEvent/` directory
  - `components/NoSSR.tsx`
  - `sentryWrapper.ts`
  - ...

- Update all imports across codebase:
  - `@calcom/core/...` → `@calcom/lib/...`
  - Affected: apps/api, apps/web, packages/features, packages/emails, etc.

- Remove `@calcom/core` from:
  - All `package.json` dependencies
  - `next.config.js` transpilePackages
  - Build configurations
  - Test mocks

- Update CODEOWNERS paths
- Merge overlapping exports in `@calcom/lib`

## Why

`@calcom/core` and `@calcom/lib` had overlapping purposes, creating:
- Confusing package boundaries
- Circular dependency risks
- Maintenance overhead
- Unclear organization for contributors

Consolidation simplifies architecture and reduces dependency graph complexity.