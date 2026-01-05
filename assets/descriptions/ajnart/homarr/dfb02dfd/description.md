# Title
-----
Migrate API endpoints to tRPC

# Summary
-------
Replaced traditional Next.js API routes with tRPC endpoints to achieve end-to-end type safety and improved developer experience across the entire API surface.

# Why
---
- Remove manual type definitions and axios/fetch calls scattered throughout the codebase
- Gain automatic type inference from server to client
- Eliminate runtime errors from API contract mismatches
- Improve maintainability with centralized API logic

# Changes
---------
**Infrastructure:**
- Added tRPC packages (`@trpc/client`, `@trpc/server`, `@trpc/next`, `@trpc/react-query`)
- Created tRPC context, router initialization, and API handler (`/api/trpc/[trpc].ts`)
- Set up client-side utilities with `api.withTRPC()` wrapper

**Routers created:**
- `app` - ping endpoint
- `config` - all/delete/save operations
- `docker` - container management (list, start/stop/restart/remove)
- `icon` - repository icons
- `dashDot` - system info & storage
- `dnsHole` - Pi-hole/AdGuard control & summary
- `download` - torrent/usenet queue info
- `mediaRequest` - Overseerr/Jellyseerr requests
- `mediaServer` - Jellyfin/Plex sessions
- `overseerr` - search/request/approve media
- `usenet` - SABnzbd/NZBGet queue/history/control
- `calendar` - media calendar aggregation
- `rss` - feed parsing

**Component updates:**
- Replaced `useQuery()` + `fetch()` with `api.<router>.<procedure>.useQuery()`
- Replaced `useMutation()` + `axios.post()` with `api.<router>.<procedure>.useMutation()`
- Removed manual error handling in favor of tRPC error handling
- Updated all widgets and settings components

**Removed:**
- `/api/modules/*` endpoints
- `/api/configs/*` endpoints  
- `/api/docker/*` endpoints
- `/api/icons/*` endpoint
- Custom fetch/axios wrappers
- Manual type definitions for API responses

**Utilities:**
- Added `checkIntegrationsType()` helper for type-safe integration checking
- Added `findAppProperty()` helper for app configuration access
- Created `DockerSingleton` for Docker client management

**Config:**
- Added `tsconfig.json` path alias `~/*` → `./src/*`
- Added `vite-tsconfig-paths` for Vitest