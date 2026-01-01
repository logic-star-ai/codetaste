# Restructure Parca UI packages

## Summary
Reorganize frontend packages to better separate concerns between React hooks and utility functions.

## Changes

### New Packages
- **`@parca/hooks`**: Centralized package for all React hooks
  - `useContainerDimensions` (moved from `@parca/dynamicsize`)
  - `useUIFeatureFlag`
  - `useUserPreference`
  - Exports `USER_PREFERENCES` constants

- **`@parca/utilities`**: Replaces `@parca/functions` with better naming
  - Time utilities (formatDate, formatDuration, convertTime, ...)
  - Value formatters
  - Color utilities (COLOR_PROFILES, diffColor, getNewSpanColor, ...)
  - String utilities (capitalize, cutToMaxStringLength, ...)
  - Binary search utilities
  - Helper functions (parseParams, convertToQueryParams, saveAsBlob, ...)

### Migration
- Update all imports from `@parca/functions` → `@parca/utilities`
- Update hook imports from `@parca/functions/*` → `@parca/hooks`
- Update `useContainerDimensions` imports from `@parca/dynamicsize` → `@parca/hooks`
- Configure build system (craco, webpack) for new packages
- Update package.json dependencies across affected packages

### Cleanup
- Remove `export` script from root package.json

## Impact
All packages importing from `@parca/functions` or using hooks need dependency updates.