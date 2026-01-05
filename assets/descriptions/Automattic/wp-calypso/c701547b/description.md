# Refactor: Split SitesOverview utils.ts into modular, organized files

## Summary
Extract all functions and constants from the monolithic `client/jetpack-cloud/sections/agency-dashboard/sites-overview/utils.ts` file into separate, focused files organized by functionality and location of use. Improve i18n practices by replacing raw `translate` calls with `useTranslate` hooks.

## Why
- The `utils.ts` file had grown too large and contained mixed concerns
- Functions were not co-located with their usage
- Raw `translate` function usage violates `i18n-calypso` best practices
- Difficult to maintain and test as a single monolithic file

## Changes

### File Organization
- Move functions to `lib/` directories for non-hook utilities
- Move React hooks to `hooks/` directories
- Co-locate utilities closer to their usage points
- Organize by feature domain (backup, boost, monitor, scan, etc.)

### New File Structure
- `lib/constants.ts` - Product slug mappings, shared constants
- `lib/boost.ts` - `getBoostRating()`, `getBoostRatingClass()`
- `hooks/use-default-site-columns.ts` - Site column definitions
- `hooks/use-notification-durations.ts` - Available notification durations
- `hooks/use-site-count-text.ts` - Site count formatting
- `site-actions/get-action-event-name.ts` - Action tracking event names
- `site-content/hooks/use-formatted-sites.ts` - Site data formatting logic
- `site-expanded-content/hooks/use-extracted-backup-title.ts` - Backup title extraction
- `site-expanded-content/hooks/use-get-monitor-downtime-text.ts` - Downtime text formatting
- `site-status-content/lib/get-links.ts` - Link generation per status
- `site-status-content/lib/get-row-event-name.ts` - Row event tracking
- `site-status-content/hooks/use-tooltip.ts` - Tooltip text generation
- `site-status-content/hooks/use-row-metadata.ts` - Row metadata computation

### i18n Migration
- Replace `translate()` calls with `useTranslate()` hook
- Convert functions to hooks where translation is needed
- Update all call sites accordingly

### Testing
- Migrate unit tests to co-locate with new files
- Update test imports and mocks
- Ensure test coverage maintained

### Cleanup
- Remove original `utils.ts` file
- Update all import statements across the codebase
- Remove unused exports and dependencies