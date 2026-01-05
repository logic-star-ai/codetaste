# Refactor: Lift layout-related components from A4A to shared location

## Summary

Relocate A4A's layout-related components to `client/layout/multi-sites-dashboard/` and rename CSS classes from `a4a-*` to `multi-sites-dashboard-layout-*` to make them reusable across different dashboard contexts.

## Why

These layout components (`Layout`, `LayoutBody`, `LayoutColumn`, `LayoutHeader`, `LayoutTop`, `LayoutNavigation`) were originally built for A4A but are generic enough to be used by other multi-site dashboards (e.g., wpcom sites dashboard, domains overview).

## Changes

**Component relocation:**
- `client/a8c-for-agencies/components/layout/*` → `client/layout/multi-sites-dashboard/*`
- Files: `body.tsx`, `column.tsx`, `header.tsx`, `index.tsx`, `nav.tsx`, `top.tsx`, `style.scss`

**CSS class renaming:**
- `.a4a-layout*` → `.multi-sites-dashboard-layout*`
- `.a4a-layout__*` → `.multi-sites-dashboard-layout__*`
- `.a4a-layout-column*` → `.multi-sites-dashboard-layout-column*`

**Import updates:**
- ~50+ files updated to use new import paths
- All references to old CSS classes updated in SCSS files

**Style separation:**
- A4A-specific styles remain in `client/a8c-for-agencies/components/layout/style.scss`
- Generic layout styles moved to `client/layout/multi-sites-dashboard/style.scss`

## Scope

Affected areas:
- A4A sections: overview, sites, team, referrals, migrations, marketplace, purchases, agency-tier, partner-directory, client
- wpcom: sites dashboard, domains management, plugins
- Shared: multi-site plugin update manager