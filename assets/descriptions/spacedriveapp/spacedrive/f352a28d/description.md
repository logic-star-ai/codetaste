# Migrate Landing Page to Next.js App Router

## Summary
Migrate `sd-landing` from Pages Router to Next.js 13 App Router, significantly reducing JavaScript bundle size and improving organization through nested layouts and better code splitting.

## Changes

### Architecture
- Migrated from `pages/` to `app/` directory structure
- Converted `_app.tsx` + `_document.tsx` → `app/layout.tsx`
- Implemented nested layouts for docs section
- Split monolithic pages into smaller client/server components

### Performance Optimizations  
- Enabled tree shaking via `sideEffects: false` in `@sd/ui` & other packages
- Separated `zxcvbn` password strength lib into own module for lazy loading
- Dynamic imports for heavy components (Space, Bubbles backgrounds)
- Moved WebGL detection to `useEffect` (client-side only)
- Added bundle analyzer
- Enabled `optimizePackageImports` for `@sd/ui`

### Component Structure
- Extracted reusable components:
  - `Background.tsx` - WebGL/fallback background
  - `Downloads.tsx` - Platform download buttons
  - `NavBar/` - Navigation with mobile dropdown
  - `Footer.tsx` - Site footer
  - `HomeCTA.tsx` - Call-to-action button
- Added `'use client'` directives where needed for interactivity

### Documentation Reorganization  
- `app/docs/[[...slug]]/` with dedicated components:
  - `Sidebar.tsx` - Doc navigation
  - `Search.tsx` - Search interface
  - `Markdown.tsx` - MDX wrapper
  - `Index.tsx` - Docs home
  - `layout.tsx` - Docs-specific layout with mobile menu

### Routing Migration
- `/blog/[slug]` → `app/blog/[slug]/page.tsx`
- `/docs/[...slug]` → `app/docs/[[...slug]]/page.tsx` (optional catch-all)
- `/team`, `/careers`, `/roadmap`, `/pricing` → `app/[route]/page.tsx`
- Proper metadata generation using Next 13 conventions

### Cleanup
- Removed database code (drizzle-orm, drizzle-kit, AWS SES)
- Removed unused `PageWrapper` component
- Updated styling imports: `@sd/ui/style` → `@sd/ui/style/style.scss`
- Moved favicon to `app/` directory
- Added `'use client'` to brand SVG exports

### Dependencies
- Next.js: `13.4.3` → `13.5.4`
- `@phosphor-icons/react`: `^2.0.10` → `^2.1.3`  
- `@icons-pack/react-simple-icons`: `^7.2.0` → `^9.1.0`
- Added `@next/bundle-analyzer`, `react-error-boundary`, `katex`

## Why
- **Smaller bundles**: Order of magnitude reduction in first-load JS
- **Better DX**: Nested layouts, automatic code splitting, cleaner structure
- **Modern patterns**: Leverage App Router's RSC and streaming capabilities
- **Improved performance**: Tree shaking, dynamic imports, optimized package imports