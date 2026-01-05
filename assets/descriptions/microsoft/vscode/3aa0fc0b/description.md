# Title
-----
Refactor smoke UI automation into separate package

# Summary
-------
Split `smoke` project into two packages: `test/smoke` (test cases + test runner) and `test/automation` (UI automation driver + component automation modules). Smoke tests now depend on automation package via local filesystem reference.

# Why
---
- Enforce clearer separation between test cases and UI automation infrastructure
- Enable reusable npm package for VS Code UI automation
- Allow first-party extensions (VS Live Share, etc.) to run UI tests against VS Code
- Facilitate easier updates to test automation when testing new VS Code releases
- No expectation of semver stability or avoiding breaking changes

# What Changed
-----------
**New Package Structure:**
- Created `test/automation/` package with own `package.json`, `README`, `tsconfig.json`
- Moved UI automation driver and per-component modules from `test/smoke/src/` to `test/automation/src/`

**Files Relocated:**
- `test/smoke/src/vscode/code.ts` → `test/automation/src/code.ts`
- `test/smoke/src/application.ts` → `test/automation/src/application.ts`
- `test/smoke/src/logger.ts` → `test/automation/src/logger.ts`
- `test/smoke/src/areas/*/` → `test/automation/src/*.ts` (flattened structure)
- Driver files (`driver.js`, puppeteer driver, etc.) → `test/automation/src/`

**Import Changes:**
- Smoke tests now import from `'vscode-automation'` instead of relative paths
- Example: `import { Application, Quality, ... } from 'vscode-automation';`

**Build Process:**
- `test/smoke` depends on `test/automation` via `link:../automation`
- Preinstall hook: `yarn --cwd ../automation` 
- Simplified smoke compile script (no longer copies driver files)

**Exports:**
- `test/automation/src/index.ts` exports all automation modules
- Exports include: Application, Code, Workbench, Editor, Explorer, Extensions, Debug, Terminal, etc.

# Dependencies
-----------
- Moved automation-specific dependencies to `test/automation/package.json`
- Removed `@types/puppeteer`, `electron` from smoke package
- Smoke package now has minimal deps + `vscode-automation` link

# Testing
-------
- Existing VS Code smoke tests verified passing with changes
- Build/watch scripts updated for two-package structure