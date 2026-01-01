# Extract URL utilities to `@automattic/calypso-url` package

## Summary

Move core URL utility functions from `client/lib/url` to new standalone package `@automattic/calypso-url` to enable reuse outside Calypso monorepo.

## Why

Enable checkout and other functionality to be packaged separately with type safety... URL utilities have minimal dependencies, making them ideal candidates for extraction.

## What Changed

- Created new `@automattic/calypso-url` package in `packages/`
- Migrated core functions:
  - `format` - Format URLs to different types (absolute → scheme-relative, etc.)
  - `getUrlParts` - Split URL into component parts
  - `getUrlFromParts` - Reconstruct URL from parts
  - `determineUrlType` - Detect URL type (ABSOLUTE, SCHEME_RELATIVE, PATH_ABSOLUTE, PATH_RELATIVE, INVALID)
  - `URL_TYPE` enum
- Updated ~50+ import statements across codebase
- Removed migrated code from `client/lib/url`
- Updated READMEs, removed migrated tests
- Fixed type imports, removed duplicate `URL` type

## Scope

Only functions required by `lib/plans` were migrated... Remaining `lib/url` utilities (with heavier dependencies) left in place for potential future migration.

## Technical Notes

- No functional changes to migrated code
- Package configured with TypeScript, ESM/CJS dual output
- All automated tests pass with updated imports