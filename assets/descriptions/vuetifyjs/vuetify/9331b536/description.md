# Refactor: Convert All Component Props to Factory Functions

## Summary
Normalize component prop generation across the entire codebase by extracting prop definitions into factory functions using `propsFactory()`.

## Why
- Inconsistent prop definition patterns across components
- Improve reusability and composability of prop definitions
- Enable better prop filtering and inheritance patterns
- Standardize how props are generated and shared

## What Changed
- Extracted all component prop definitions into `makeV*Props()` factory functions
- All factory functions now use `propsFactory()` utility
- Components updated to consume props via `props: makeV*Props()`
- Pattern applied consistently across ~100+ components:
  - `VAlert`, `VApp`, `VAppBar`, `VAutocomplete`, ...
  - `VDataTable` and all related subcomponents
  - All lab components (`VInfiniteScroll`, `VSkeletonLoader`, ...)
  - Transition components

## Structure
```ts
// Before
export const VComponent = genericComponent()({
  props: {
    someProp: String,
    ...makeOtherProps(),
  }
})

// After  
export const makeVComponentProps = propsFactory({
  someProp: String,
  ...makeOtherProps(),
}, 'v-component')

export const VComponent = genericComponent()({
  props: makeVComponentProps(),
})
```

## Benefits
- Props can be easily filtered via `VComponent.filterProps()`
- Better TypeScript inference
- Easier to compose and extend prop definitions
- Consistent pattern for all components