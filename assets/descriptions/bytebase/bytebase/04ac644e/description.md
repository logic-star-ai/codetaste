# Refactor: Use route names instead of paths

## Summary
Refactor routing system to use route name constants instead of hardcoded path strings throughout the application. Rename project route constants to include `_ROUTE_` prefix and extract workspace setting route names into centralized constants.

## Why
- **Maintainability**: Route names are more stable than paths when structure changes
- **Type safety**: Centralized constants prevent typos and enable better IDE support
- **Consistency**: Uniform approach to navigation across the codebase
- **Refactoring**: Easier to update routes without breaking references

## Changes

### Route Constants Renamed
- Add `_ROUTE_` prefix to all project route constants for clarity
  - `PROJECT_V1_BRANCHES` → `PROJECT_V1_ROUTE_BRANCHES`
  - `PROJECT_V1_WEBHOOK_DETAIL` → `PROJECT_V1_ROUTE_WEBHOOK_DETAIL`
  - `PROJECT_V1_CHANGELIST_DETAIL` → `PROJECT_V1_ROUTE_CHANGELIST_DETAIL`
  - ... (all project routes)

### Setting Routes Centralized
- Extract all workspace setting route names to constants in `workspaceSetting.ts`
  - `SETTING_ROUTE_WORKSPACE_GENERAL`
  - `SETTING_ROUTE_WORKSPACE_SSO`
  - `SETTING_ROUTE_WORKSPACE_SQL_REVIEW`
  - ... (all setting routes)

### Navigation Refactored
- Replace `router.push({ path: "/..." })` with `router.push({ name: ROUTE_NAME })`
- Replace hardcoded route name strings with constants
- Update all `router-link :to="..."` to use route names
- Update permission checks to use route name constants

### Component Updates
- `CommonSidebar`: Support route names in item definitions
- `ProjectSidebarV1`: Use route names + support Ctrl/Cmd+Click for new tab
- Extract `WebhookTypeIcon` component (side refactor)

### Files Updated
- 50+ component files updated to use route name constants
- Route definition files: `projectV1.ts`, `workspaceSetting.ts`, `database.ts`, `environment.ts`
- Utility files: `role.ts` permission checks