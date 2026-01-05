# Refactor button styles to use standardized classes

## Summary
Remove redundant CSS styles and replace custom button implementations with proper design system classes (`btn-primary`, `btn-secondary`, `btn-tertiary`, `btn-sm`, `btn-xs`, `btn-lg`, etc.) throughout the application.

## Why
- Inconsistent button styling across different components
- Duplicate CSS rules overriding base button styles
- Custom button styles scattered throughout component-specific SCSS files
- Maintenance overhead from redundant style definitions

## Changes Made

### Removed redundant CSS
- Custom button styles in billing/subscriptions, feature discovery, license settings
- Duplicate padding/border/color definitions
- Component-specific button overrides that duplicated base styles
- Removed `contact_us.scss` entirely

### Updated button implementations
- Actions menu: `btn-primary btn-sm` for marketplace button
- Billing pages: Standardized upgrade, contact sales, and cancel buttons
- License settings: Updated add seats, upload license, contact us buttons
- IP filtering modals: Save/cancel/delete buttons using proper classes
- Permission schemes: Cancel buttons with `btn-tertiary`
- Announcement bars: `btn-xs btn-inverted` for CTA buttons
- Data retention forms: Standardized cancel/save buttons
- Trial/renewal cards: Consistent button sizing and variants

### Test updates
- Updated E2E selectors to use `data-testid` attributes
- Fixed snapshot tests for new button classes
- Updated selectors from icon classes to proper test IDs

### Style improvements
- Fixed hover states on save panel error state
- Tweaked disabled state styling on floating save bar
- Adjusted button font sizes (xs = 12px)
- Scoped CSS to avoid affecting product switcher