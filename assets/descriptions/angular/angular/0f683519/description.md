# Refactor: Extract web worker platform into separate packages

## Summary
Move web worker platform code from `@angular/platform-browser` and `@angular/platform-browser-dynamic` into two new dedicated packages: `@angular/platform-webworker` and `@angular/platform-webworker-dynamic`.

## Why
- Improve modularity and separation of concerns
- Reduce bundle size for non-webworker applications
- Make webworker platform a distinct, opt-in feature
- Remove unnecessary `@angular/compiler` dependency from `@angular/platform-browser`

## Changes

**New Packages Created:**
- `@angular/platform-webworker` - Core webworker platform functionality
- `@angular/platform-webworker-dynamic` - Dynamic compilation support for webworkers

**Code Migration:**
- Move `web_workers/` directory from platform-browser to platform-webworker
- Move `worker_app.ts` and `worker_render.ts` to platform-webworker
- Move `platformWorkerAppDynamic` and `bootstrapWorkerUi` to appropriate packages
- Relocate webworker-related types: `ClientMessageBroker`, `ServiceMessageBroker`, `MessageBus`, `WORKER_*` tokens, etc.

**Public API Updates:**
- Remove webworker exports from `@angular/platform-browser` and `@angular/platform-browser-dynamic`
- Export webworker APIs from new packages
- Update API guard files

**Build Configuration:**
- Add new packages to build scripts (build.sh, gulpfile.js)
- Create rollup.config.js and tsconfig.json for both packages
- Update SystemJS configuration in playground

**Internal Refactoring:**
- Add private import files for cross-package access to internal APIs
- Update `__platform_browser_private__` to expose additional internal APIs needed by webworker packages
- Remove `@angular/compiler` from platform-browser peer dependencies

**Test & Example Updates:**
- Update all playground examples to import from new packages
- Migrate webworker tests to new package locations
- Update test configuration (test-main.js)

## Breaking Change
Web worker platform is now exported via `@angular/platform-webworker` and `@angular/platform-webworker-dynamic` instead of `@angular/platform-browser` / `@angular/platform-browser-dynamic`.