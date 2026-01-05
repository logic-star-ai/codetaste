# Migrate functions data to Astro Content Collections API

## Summary

Redesign the code that processes function data from typedoc to use Astro's Content Collections API (v2), decoupling typedoc parsing from the rest of the docs system and enabling dynamic HMR-like reloading when editing library source files.

## Why

- Current system uses pre-generated JSON files (`data.json`) that require manual rebuild
- Transform logic is tightly coupled to the docs build process
- No hot module reloading when editing library source files
- Parsing logic is centralized, making it inflexible for component-specific rendering needs

## Changes

### Core Architecture
- Replace custom transform files (`lib/transform.ts`, `lib/v1/transform.ts`) with Content Collections
- Create `typedocLoader` to run typedoc as an Astro loader instead of CLI utility
- Define schemas using Zod for functions, categories, and mapping entries
- Move parsing logic from centralized transforms to individual components

### Content Collections
- **functions**: Main library functions loaded dynamically from typedoc
- **functions-v1**: Legacy v1 functions with separate loader
- **categories-v1**: V1 category organization
- **mapping**: Migration mappings for other libraries (lodash, etc.)

### Data Flow
- Remove intermediate `src/data/data.json` files
- Run typedoc via API during Astro build/dev
- Enable watch mode for source file changes with incremental updates
- Parse typedoc output directly into Content Collections

### Component Updates
- Extract parameter rendering to `<Parameters>` component
- Extract return type logic to `<FunctionReturnType>` component  
- Update `<FunctionCard>`, `<FunctionApi>`, etc. to use new data structure
- Move tag extraction (`@dataFirst`, `@lazy`, etc.) to reusable utilities

### Build Process
- Remove `npm run typedoc` pre-build step
- Remove `build:all` command (now just `build`)
- Integrate typedoc execution into Astro's build via vite plugin
- Implement static scripts plugin for standalone browser scripts

### Developer Experience
- HMR for library source file changes in dev server
- Type-safe schema validation for all content
- Better separation between data loading and presentation
- Clearer file organization with content collections

## Technical Details

- Custom typedoc loader in `lib/typedoc/loader.ts` using `Application.convertAndWatch()`
- Zod schemas in `lib/typedoc/schema.ts` for type safety
- V1 loaders use file-based approach with existing `functions.json`
- Tag extraction utilities in `lib/tags.ts` for `@category`, `@signature`, etc.
- Routing logic updated to fetch collections dynamically per page