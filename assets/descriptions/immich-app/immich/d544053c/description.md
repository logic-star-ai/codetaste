# Title
Migrate CircleIconButton to @immich/ui IconButton

# Summary
Replace custom `CircleIconButton` component with standardized `IconButton` from `@immich/ui` library across the entire web codebase.

# Why
- Consolidate button implementations using shared UI library
- Standardize component API and behavior
- Reduce custom component maintenance burden

# Changes
- Remove `CircleIconButton` component and associated tests
- Update all `CircleIconButton` usages to `IconButton` with new props:
  - `title` → `aria-label`
  - Add `shape="round"` for circular appearance
  - Update `size` values (e.g., `"16"` → `"small"`, `"20"` → `"medium"`)
  - Replace `color` values (`"opaque"` → `"secondary"`, etc.)
  - Add `variant` prop (typically `"ghost"`)
  - Remove custom `padding` prop
- Update `CastButton` to remove `whiteHover` and `navBar` props
- Use `ThemeSwitcher` from UI lib instead of custom implementation
- Apply `dark` class for forced dark mode in asset viewer, slideshow bar, and memory viewer contexts
- Simplify `ButtonContextMenu` props to align with new `IconButton` API

# Impact
- ... album pages, asset viewer, faces/people management, search, settings, shared links, navigation bar, modals, upload panel, ...
- No functional changes, purely UI component migration
- All button interactions and accessibility features preserved