# Refactor: Remove `<Box>` and `sx` prop usage throughout codebase

## Summary

Replace all Material-UI `<Box>` components and `sx` props with native HTML elements and emotion's `css` prop. Improve TypeScript typing consistency across components.

## Changes

**Styling System:**
- Replace all `<Box>` → native HTML (`<div>`, `<span>`, etc.)
- Replace all `sx` props → `css` prop (emotion)
- Remove `@mui/styles` package dependency
- Add ESLint rule to prevent future `<Box>` usage

**Type System:**
- Use `FC` type consistently for component declarations
- Break inline type definitions into named interfaces
- Replace `BoxProps` → `HTMLAttributes<HTMLDivElement>`
- Add explicit prop type interfaces for clarity
- Use `type` imports where appropriate

**Component Props:**
- Convert `sx` style objects → `css` style objects
- Replace `component="..."` → native elements
- Update margin/padding: `px={2}` → `padding: 16`
- Replace MUI-specific values: `borderRadius: 1` → `borderRadius: 8`

**Theme Access:**
- Use `useTheme()` hook instead of inline `(theme) => ...` where beneficial
- Keep inline theme callbacks where appropriate for colocation

## Affected Areas

- Dashboard layout & navigation
- Filter components
- Tables & data display
- Form components
- Settings pages
- Workspace pages
- Alert/notification components
- Various utility components

## Why

- Reduce dependency on MUI's proprietary styling system
- Use standard emotion styling approach
- Improve TypeScript type safety and consistency
- Potentially reduce bundle size
- Simplify component APIs (fewer MUI-specific patterns)
- Better alignment with modern React/emotion patterns