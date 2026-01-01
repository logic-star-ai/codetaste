# Refactor: Align project structure with Angular 2 conventions

## Summary
Major refactoring to modernize the AngularJS codebase by adopting Angular 2+ conventions and ES6 module system. This prepares the codebase for future Angular migration while improving maintainability.

## Why
- Current IIFE-wrapped modules hinder code organization and tree-shaking
- Legacy var declarations instead of let/const
- Per-file module definitions create coupling via string-based dependencies
- Project structure doesn't follow Angular 2 conventions
- Template loading via URL strings instead of webpack

## Changes

**Module System**
- Remove IIFE wrappers from TypeScript files
- Replace per-file AngularJS modules with ES6 exports/imports
- Wire up modules using imports/exports instead of string names
- Add `.module.ts` suffix to module files
- Implement manual bootstrap process (remove ng-app)

**Code Quality**
- Rewrite all `var` declarations to `let`/`const` in TypeScript
- Use ES6 imports throughout

**Project Structure**
- Remove `timesketch/ui/static/components/` directory (flatten structure)
- Move templates: `timesketch/ui/templates/` → `timesketch/templates/`
- Move views: `timesketch/ui/views/` → `timesketch/views/`
- Move static assets: `timesketch/ui/static/{fonts,img}/` → `timesketch/static/{fonts,img}/`
- Align file names with Angular 2 naming convention

**Build System**
- Replace `@ultimate/aot-loader` with `@ngtools/webpack`
- Load AngularJS templates with webpack `raw-loader` (require() instead of templateUrl)
- Update webpack config for new paths
- Add Angular 5.0.0-beta.5 dependencies (preparation for migration)

**Configuration**
- Update `.gitignore`, `MANIFEST.in`, `setup.py`, `tsconfig.json` for new paths
- Update Python imports for relocated views