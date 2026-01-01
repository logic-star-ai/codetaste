# Title
-----
Refactor: Split `loggedInViewer` tRPC router into focused sub-routers

# Summary
-------
The `loggedInViewer` tRPC router has grown too large, importing excessive dependencies and causing performance issues. Split it into smaller, focused routers (`me`, `i18n`) to reduce bundle size and improve load times per endpoint.

# Why
---
- `loggedInViewer` router imports tons of dependencies, loading unnecessary code for each tRPC call
- Poor code organization with unrelated procedures grouped together
- Performance bottleneck due to monolithic router structure

# Changes
---------

**New Router Structure:**
- `viewer.me.*` - User-specific queries/mutations (`get`, `deleteMe`, `deleteMeWithoutPassword`, `myStats`, `platformMe`, `bookingUnconfirmedCount`, `shouldVerifyEmail`, `getUserTopBanners`)
- `viewer.i18n.*` - Internationalization queries (`get`)

**API Routes:**
- `/api/trpc/me/[trpc].ts` - New endpoint for `me` router
- `/api/trpc/i18n/[trpc].ts` - New endpoint for `i18n` router

**File Migrations:**
- Move handlers from `routers/loggedInViewer/*` to `routers/viewer/me/*` and `routers/viewer/i18n/*`
- Move `i18n` from `publicViewer` to dedicated `viewer/i18n` router

**Updated Calls:**
- `viewer.me` → `viewer.me.get`
- `viewer.bookingUnconfirmedCount` → `viewer.me.bookingUnconfirmedCount`
- `viewer.getUserTopBanners` → `viewer.me.getUserTopBanners`
- `viewer.shouldVerifyEmail` → `viewer.me.shouldVerifyEmail`
- `viewer.deleteMe` → `viewer.me.deleteMe`
- `viewer.deleteMeWithoutPassword` → `viewer.me.deleteMeWithoutPassword`
- `viewer.myStats` → `viewer.me.myStats`
- `viewer.platformMe` → `viewer.me.platformMe`
- `viewer.public.i18n` → `viewer.i18n.get`

**SSR Updates:**
- Update `ssrInit` and server-side prefetch calls
- Fix type references across codebase

**Cache Configuration:**
- Update cache headers in `createNextApiHandler` for new routes

# Testing
---------
- [ ] All tRPC routes functional
- [ ] SSR hydration works correctly
- [ ] Type checking passes
- [ ] E2E tests pass (auth, locale, etc.)
- [ ] No performance regression