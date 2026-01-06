# Refactor code organization for improved code splitting

Major refactoring to improve code organization and enable better code splitting by:
- Moving shared utilities from `site` to `common` module
- Consolidating scattered `userComplete` functionality into single location
- Reducing reliance on global `site` object
- Making dependencies explicit through direct imports