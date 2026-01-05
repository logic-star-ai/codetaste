# Enable `noImplicitAny` and add explicit type declarations

## Summary
Enable TypeScript's `noImplicitAny` compiler option and add explicit type annotations throughout the codebase for stricter type checking.

## Why
Currently many variables/parameters have implicit `any` types, bypassing type checking. Explicit types catch errors at compile time and prevent bugs.

## Changes Required
- Add `"noImplicitAny": true` to `src/tsconfig.json`
- Add explicit type annotations across codebase:
  - Background scripts: config-manager, extension, messenger, newsmaker, tab-manager, user-storage, ...
  - Inject scripts: dynamic-theme, css-collection, inline-style, modify-css, network, style-manager, variables, ...
  - UI components: popup pages/components, devtools, controls (select, text-list, color-picker), ...
  - Utils: time, url, extension-api, ...
  - Tests: config, locales, color, time, ...
- Define interfaces where needed (e.g., `Config` interface)
- Annotate:
  - Function parameters & return types
  - Variable declarations
  - Object properties & map types
  - Callback signatures
  - Generic types

## Verification
No runtime changes—compiled output identical before/after (verified with `diff -r`). Purely type annotation changes.