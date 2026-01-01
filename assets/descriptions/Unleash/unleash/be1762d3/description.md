# Refactor: Migrate components from `useStyles` to `styled` components and `sx` props (Batch 3)

## Summary

Refactor 20+ components away from `makeStyles`/`useStyles` pattern to use Material-UI v5's `styled()` API and `sx` props for styling.

## Why

- Align with Material-UI v5 best practices
- Improve performance by using CSS-in-JS via `styled()` instead of class-based styles
- Better TypeScript support with `styled()` components
- Reduce bundle size by eliminating `makeStyles` usage

## Components Refactored

- `Search` → styled components + `sx`
- `SearchField` → **deleted** (deprecated)
- `SegmentItem` → styled components
- `SkipNavLink` → styled components + reorganized to dedicated directory
- `StrategyItemContainer` → styled components + `sx`
- `Table/*` components:
  - `ActionCell`, `FeatureSeenCell`, `FeatureTypeCell`, `HighlightCell`, `LinkCell`, `TextCell`
  - `SortableTableHeader`, `CellSortable`, `SortArrow`
  - `Table`, `TableCell`, `TablePlaceholder`, `VirtualizedTable`
- `TabNav` → `sx` props
- `ToastRenderer` + `Toast` → removed classes
- `AnimateOnMount` → refactored to use inline `CSSProperties` instead of class names

## Changes

- Deleted `.styles.ts` files for all affected components
- Converted `makeStyles()` → `styled()` components with proper prop forwarding
- Replaced `className` + `useStyles()` → `sx` props where appropriate
- Updated `AnimateOnMount` API to accept `CSSProperties` objects instead of CSS class strings
- Extracted reusable style objects (e.g., `fadeInBottomEnter`, `wrapperStyles`) to `themeStyles.ts`
- Fixed theme spacing/color references to use proper theme tokens

## Technical Details

- Used `styled()` with `shouldForwardProp` to prevent DOM warnings
- Converted shorthand `sx` props (`ml`, `mr`) → explicit properties (`marginLeft`, `marginRight`)
- Maintained existing functionality while improving type safety
- Updated snapshots for test compatibility