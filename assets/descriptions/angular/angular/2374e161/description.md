Title
-----
Refactor: Extract HTTP module to top-level standalone package

Summary
-------
Extract HTTP functionality from `angular2/` module into a separate top-level `http/` module/package. This involves moving all HTTP-related source files, tests, and creating independent package configuration.

Changes
-------

**File Structure**
- Move `modules/angular2/http.ts` → `modules/http/http.ts`
- Move `modules/angular2/src/http/**` → `modules/http/src/**`
- Move `modules/angular2/test/http/**` → `modules/http/test/**`
- Create new package files: `modules/http/package.json`, `modules/http/pubspec.yaml`
- Remove HTTP exports from `angular2/angular2.ts`, `angular2/angular2_exports.ts`, `angular2/bootstrap.ts`

**Import Path Updates**
- Update all imports from `angular2/http` → `http/http`
- Update all imports from `angular2/src/http/*` → `http/src/*`
- Update affected files: examples, tests, documentation configs

**Build System**
- Add separate bundling tasks for http module (dev/prod/min/sfx variants)
- Update gulp watch patterns to include `modules/http/**`
- Update CJS test patterns, TypeScript definition generation
- Add http to node tree build configuration
- Update test-main.js SystemJS paths

**Publishing**
- Add http module to npm publish script
- Add http module to pub publish script (commented out)

**Documentation**
- Update public-docs-package to reference `http/http.ts`
- Update typescript-definition-package with http namespace config

Closes #2680, #3417