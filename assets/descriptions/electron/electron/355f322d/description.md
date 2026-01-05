Title
-----
Move spec helper modules to `spec/lib` subdirectory

Summary
-------
Reorganize test helper modules by moving them from `spec/` root into `spec/lib/`:
- `events-helpers.ts`
- `screen-helpers.ts`
- `spec-helpers.ts`
- `video-helpers.js`
- `window-helpers.ts`

Update all import statements across spec files from `./helpers` → `./lib/helpers`

Why
---
Improves navigation and organization of the test suite by separating utility/helper modules from actual test files.

Implementation Details
----------------------
- Move helper files to new `spec/lib/` directory
- Update ~50 spec files to import from `./lib/...` instead of `./...`
- Adjust internal paths in helpers (e.g., `__dirname` references) to account for new subdirectory depth
- No functional changes to test code or helpers

Notes
-----
Pure refactoring, no behavior changes