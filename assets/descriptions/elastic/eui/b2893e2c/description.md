# Emotion Conversion: EuiSteps Component

## Summary

Convert `EuiSteps` component from Sass/SCSS to Emotion (CSS-in-JS) styling system.

## Scope

- `EuiStep`
- `EuiStepNumber` 
- `EuiStepHorizontal`
- `EuiStepsHorizontal`
- `EuiSubSteps`

## Changes

### Styling Migration

- Remove all Sass files:
  - `_index.scss`, `_mixins.scss`, `_step_number.scss`, `_steps.scss`, `_steps_horizontal.scss`, `_sub_steps.scss`, `_variables.scss`
- Create Emotion style files:
  - `step.styles.ts`
  - `step_number.styles.ts`
  - `step_horizontal.styles.ts`
  - `steps_horizontal.styles.ts`
  - `sub_steps.styles.ts`
- Remove component from `src/components/index.scss`
- Delete Amsterdam theme overrides (`src/amsterdam/overrides/_steps.scss`)

### Component Updates

- Integrate `useEuiTheme` hook in all components
- Apply styles via `css` prop
- Convert global Sass vars/mixins to JS (e.g., `$euiSize` → `euiTheme.size.base`)
- Replace `calc()` with `mathWithUnits` where applicable
- Convert to logical CSS properties (`-inline`, `-block`)

### Code Quality

- Reduce CSS specificity ... remove unnecessary nesting/chaining
- Wrap animations/transitions in `euiCanAnimate`
- Clean up modifier classNames ... convert to status-based styles
- Simplify JSX ... remove unnecessary Fragments/divs
- Convert example files from `.js` to `.tsx`

### Design Fixes

- Fix step title alignment with icon (#5847)
- Adjust padding on `s` sized titles for better text centering
- Remove unnecessary shadow on current step numbers
- Change font-weight to medium

### Testing

- Add `shouldRenderCustomStyles()` tests for all components
- Update snapshots to reflect new Emotion classNames

### Breaking Changes

Remove Sass variables (no longer needed):
- `$euiStepStatusColorsToFade`
- `$euiStepNumberSize` 
- `$euiStepNumberSmallSize`
- `$euiStepNumberMargin`

## Technical Details

- Use `euiStepVariables()` helper for consistent sizing
- Create separate style functions for different component parts (content, title, number)
- Map step statuses to appropriate theme colors via `euiButtonFillColor`
- Centralize status-to-icon/label mappings
- Use `data-step-status` attribute for test selectors