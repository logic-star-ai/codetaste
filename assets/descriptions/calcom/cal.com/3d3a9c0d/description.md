# Title
Move `classNames` utility from `@calcom/lib` to `@calcom/ui`

# Summary
Relocate the `classNames` utility function from the `@calcom/lib` package to `@calcom/ui` package to reduce cross-package dependencies and improve package organization.

# Why
- Part of effort to remove `@calcom/lib` references from `@calcom/ui`
- `classNames` is primarily UI-focused (uses `tailwind-merge` for CSS class manipulation)
- Better separation of concerns: UI utilities should live in UI package
- Reduces circular/unnecessary dependencies between core packages

# Changes
- Move `packages/lib/classNames.ts` → `packages/ui/classNames.ts`
- Update 100+ import statements across codebase:
  - `@calcom/lib/classNames` → `@calcom/ui/classNames`
  - `@calcom/lib` (destructured) → `@calcom/ui/classNames`
- Migrate `tailwind-merge` dependency from `@calcom/lib` to `@calcom/ui`
- Remove `classNames` export from `@calcom/lib/index.ts`
- Add `./classNames` export to `@calcom/ui/package.json`
- Delete redundant `apps/web/lib/classNames.ts` re-export file

# Affected Areas
- Apps: storybook, web
- Packages: app-store, features (bookings, calendars, ee/*, eventtypes, filters, ...), platform, ui
- ~100+ files updated with new import paths