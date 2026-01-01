# Clean up unnecessary `RouterContextFixture` usage in tests

## Summary
Remove redundant `RouterContextFixture` usage across test files. Most tests no longer need explicit router context injection.

## Why
1. **Misnomer** - `RouterContextFixture` injects organization + project legacy context, not just React Router context
2. **Obsolete** - Organization legacy context no longer exists; customization via this fixture is pointless
3. **Redundant** - `render()` already injects legacy context by default; passing unmodified fixtures is unnecessary

## Changes
- Remove `RouterContextFixture` imports from ~50+ test files
- Remove `context: routerContext` / `context: RouterContextFixture()` from render calls
- Remove organization from `RouterContextFixture([{organization}])` where fixture is still needed
- Clean up: `access.spec.tsx`, `feature.spec.tsx`, `role.spec.tsx`, `assigneeSelectorDropdown.spec.tsx`, `badge/*.spec.tsx`, `events/interfaces/*.spec.tsx`, `discover/*.spec.tsx`, `performance/*.spec.tsx`, `settings/*.spec.tsx`, `replays/*.spec.tsx`, etc.

## Result
Cleaner, more maintainable tests without unnecessary fixture overhead.