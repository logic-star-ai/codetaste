# Move app schema to SDK package

## Summary

Relocate core app schema definitions from `@webstudio-is/project-build` to `@webstudio-is/sdk` package to improve package organization and enable CLI decoupling from Prisma.

## Why

- CLI needs to be decoupled from Prisma and unrelated packages
- Schema definitions are foundational types that should live in the SDK
- Reduces unnecessary dependencies for CLI and other consumers

## What Changed

**Moved schema files from `project-build/src/schema/` to `sdk/src/schema/`:**
- `breakpoints.ts`
- `data-sources.ts`
- `deployment.ts`
- `instances.ts`
- `pages.ts`
- `props.ts`
- `style-source-selections.ts`
- `style-sources.ts`
- `styles.ts`

**Updated imports throughout:**
- Builder app features (breakpoints, inspector, settings-panel, style-panel, workspace, sidebar-left)
- Canvas features (text-editor, webstudio-component)
- Shared utilities (nano-states, copy-paste, tree-utils, instance-utils)
- React SDK (component-renderer, context, css/style-rules, embed-template, props, tree/...)
- CLI prebuild

**Kept in `@webstudio-is/project-build`:**
- Utility functions (`findTreeInstanceIds`, `findPageByIdOrPath`, etc.)
- Database layer (parsers/serializers)
- Build type definitions

**Package updates:**
- Added `@webstudio-is/sdk` dependency to `@webstudio-is/project-build`
- Added `@webstudio-is/css-data` dependency to `@webstudio-is/sdk`