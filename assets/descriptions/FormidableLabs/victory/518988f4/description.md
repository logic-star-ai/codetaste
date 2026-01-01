# Remove prop-types from packages

## Summary
Remove `prop-types` package dependency and all PropTypes validation from Victory components across ~29 packages. TypeScript types remain as the single source of truth for type validation.

## Why
- Duplicate type definitions: Components define both TypeScript types AND PropTypes
- Runtime overhead: PropTypes validation runs in production builds
- Maintenance burden: Two systems need synchronization
- TypeScript provides compile-time type safety

## What Changed
- Removed `prop-types` package from dependencies across all packages
- Deleted all `Component.propTypes = {...}` declarations
- Removed custom PropTypes validators (`victory-core/src/victory-util/prop-types.ts`)
  - `deprecated()`, `allOfType()`, `nonNegative`, `integer`, `greaterThanZero`, `domain`, `scale`, `homogeneousArray`, `matchDataLength`, `regExp`
- Removed `CommonProps.baseProps`, `CommonProps.dataProps`, `CommonProps.primitiveProps` 
- Removed PropTypes exports from `victory-core` and `victory-native`
- Deleted PropTypes tests (`prop-types.test.ts`)
- Updated ESLint config: moved `react/prop-types: off` rule to TypeScript files only
- Removed `eslint-disable react/prop-types` comments where no longer needed

## Affected Packages
victory, victory-area, victory-axis, victory-bar, victory-box-plot, victory-brush-container, victory-brush-line, victory-candlestick, victory-canvas, victory-chart, victory-core, victory-cursor-container, victory-errorbar, victory-group, victory-histogram, victory-legend, victory-line, victory-native, victory-pie, victory-polar-axis, victory-scatter, victory-selection-container, victory-shared-events, victory-stack, victory-tooltip, victory-voronoi, victory-voronoi-container, victory-zoom-container, docs

## Technical Details
- TypeScript interfaces remain unchanged and provide type safety
- No runtime type validation in production builds
- Breaking: Consumers relying on PropTypes warnings will need TypeScript or manual validation