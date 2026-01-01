# Refactor: Reorganize tRPC routers to slim down loggedInViewer

## Summary

Slim down the `loggedInViewer` router by extracting handlers into domain-specific routers for better organization and performance.

## What Changed

Moved handlers from `loggedInViewer` to appropriate routers:

**New Routers Created:**
- `viewer.calendars` - calendar operations (`connectedCalendars`, `setDestinationCalendar`)
- `viewer.calVideo` - video recording operations (`getCalVideoRecordings`, `getDownloadLinkOfCalVideoRecordings`)
- `viewer.credentials` - credential management (`delete`)

**Relocated to Existing Routers:**
- `updateProfile` → `viewer.me.updateProfile`
- `workflowOrder` → `viewer.workflows.workflowOrder`
- `locationOptions` → `viewer.apps.locationOptions`

## Implementation Details

- Created new API endpoints: `/api/trpc/{calVideo,calendars,credentials}/[trpc].ts`
- Updated all tRPC query/mutation calls across components to use new paths
- Updated handler imports and router references
- Added new endpoints to `ENDPOINTS` array in `react/shared.ts`
- Updated tests and E2E specs to reflect new paths

## Files Affected

- Components: `CalendarListContainer`, `MultiDisconnectIntegration`, `UserProfile`, `UsernameTextfield`, settings pages...
- Router structure: `_router.tsx` files for `loggedInViewer`, `viewer`, `calendars`, `calVideo`, `credentials`, `apps`, `me`, `workflows`
- Handler/schema files relocated to new directory structure
- E2E tests: `change-username.e2e.ts`, `locale.e2e.ts`, `profile.e2e.ts`