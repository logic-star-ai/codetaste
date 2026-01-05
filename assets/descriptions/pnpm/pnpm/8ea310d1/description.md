# Rename "importers" & "workspace packages" terminology to "projects"

## Summary
Refactor codebase terminology to use "project" instead of "importer" and "workspace package" for better clarity and consistency across the entire monorepo.

## Scope

**Type/Interface Renames:**
- `WsPkg` → `Project`
- `WorkspacePackage` → `Project`  
- `ImporterManifest` → `ProjectManifest`
- `LockfileImporter` → `ProjectSnapshot`
- `WsPkgsGraph` → `ProjectsGraph`
- `ImportersOptions` → `ProjectOptions`
- `MutatedImporter` → `MutatedProject`

**Variable/Parameter Renames:**
- `importers` → `projects`
- `importerDir` → `projectDir`
- `allWsPkgs` → `allProjects`
- `selectedWsPkgsGraph` → `selectedProjectsGraph`
- `writeImporterManifest` → `writeProjectManifest`
- `lockfileImporter` → `projectSnapshot`

**Package Renames:**
- `@pnpm/read-importer-manifest` → `@pnpm/read-project-manifest`
- `@pnpm/read-importers-context` → `@pnpm/read-projects-context`
- `@pnpm/write-importer-manifest` → `@pnpm/write-project-manifest`

**Function Renames:**
- `readImporterManifest()` → `readProjectManifest()`
- `readImportersContext()` → `readProjectsContext()`
- `writeImporterManifest()` → `writeProjectManifest()`
- `readWsPkgs()` → `readProjects()`
- ...and all related utility functions

## Files Affected
- ~50+ packages across the monorepo
- Type definitions in `@pnpm/types`
- Core packages: config, get-context, headless, supi, etc.
- Plugin commands: installation, listing, outdated, publishing, rebuild, script-runners
- Tests throughout
- Documentation/READMEs

## Implementation Notes
- Pure refactoring - no functional changes
- Update all imports/exports
- Update package.json dependencies
- Update lockfile references
- Maintain backward compatibility where needed via deprecation warnings (if applicable)