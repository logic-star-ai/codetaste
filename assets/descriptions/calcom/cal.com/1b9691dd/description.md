# Refactor: Standardize /insights booking charts to use InsightsBookingService

## Summary

Refactor booking charts on `/insights` page to use standardized `InsightsBookingService` architecture, replacing custom data fetching implementations with consistent, maintainable patterns.

## Why

- Inconsistent data fetching patterns across charts
- Logic scattered between tRPC handlers and components
- Difficult to maintain and extend with new charts
- Performance improvements needed (raw SQL queries)

## Changes

**Architecture**
- Centralized data fetching logic in `InsightsBookingService`
- Introduced `createInsightsBookingService()` helper for consistency
- Created `useInsightsBookingParameters()` hook for unified parameter handling

**File Organization**
- Restructured components: `components/booking/` and `components/routing/`
- Split utilities: extracted date/time functions to `insightsDateUtils.ts`
- Renamed `TotalUserFeedbackTable` → `UserStatsTable`
- Added developer guide: `HOW_TO_ADD_BOOKING_CHARTS.md`

**Component Updates**
- All booking charts use `useInsightsBookingParameters()` hook
- Increased cache time: `staleTime: 180000` (3min)
- Added `"use client"` directives where needed
- Disabled `refetchOnWindowFocus` for better UX

**Backend Changes**
- Renamed tRPC handlers:
  - `eventsByStatus` → `bookingKPIStats`
  - `popularEventTypes` → `popularEvents`
- New service methods: `getPopularEventsStats()`, `getMembersStatsWithCount()`, `getMembersRatingStats()`, `getRecentRatingsStats()`, `getBookingStats()`, `calculatePreviousPeriodDates()`
- Simplified tRPC handlers (delegate to service layer)
- Optimized queries with raw SQL for better performance

**Testing**
- Updated test imports to reflect new file structure
- All existing functionality preserved