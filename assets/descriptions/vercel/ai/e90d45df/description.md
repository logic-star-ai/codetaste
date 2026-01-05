# Move utilities to `src/util` directory

## Summary

Consolidate utility files from multiple locations (`core/util/`, `util/`, `core/prompt/`) into a unified `src/util/` directory within the `ai` package.

## Why

Source files in the `ai` package need to be properly organized under the `src/` directory structure for better maintainability and clarity.

## Changes

- Move utilities from `packages/ai/core/util/*` → `packages/ai/src/util/*`
- Move utilities from `packages/ai/util/*` → `packages/ai/src/util/*`
- Move `prepareRetries` from `packages/ai/core/prompt/` → `packages/ai/src/util/`
- Update all import paths across the codebase to reflect new locations
- Update exports in `src/util/index.ts` and other index files

## Files Affected

Utilities being moved include:
- `async-iterable-stream.ts`
- `cosine-similarity.ts`
- `create-resolvable-promise.ts`
- `create-stitchable-stream.ts`
- `deep-partial.ts`
- `delayed-promise.ts`
- `detect-media-type.ts`
- `download.ts`
- `parse-partial-json.ts`
- `prepare-headers.ts`
- `prepare-retries.ts`
- ... and ~20 other utility files

Import statements updated in:
- `core/embed/*`
- `core/generate-*/*`
- `core/middleware/*`
- `core/prompt/*`
- `src/data-stream/*`
- `src/text-stream/*`
- `src/ui/*`
- ... and test files