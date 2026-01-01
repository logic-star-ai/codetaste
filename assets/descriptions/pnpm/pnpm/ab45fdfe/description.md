# Introduce branded types for project root directory paths

## Summary

Replace plain `string` types with branded `ProjectRootDir` and `ProjectRootDirRealPath` types throughout the codebase for improved type safety.

## Why

Plain strings used for paths can be interchangeably assigned, making it easy to accidentally pass the wrong path type to functions. Branded types provide compile-time guarantees that the correct path type is being used where expected.

## Changes

- Add `ProjectRootDir` and `ProjectRootDirRealPath` branded string types in `@pnpm/types`
- Update interfaces across packages:
  - `Project`, `ProjectsGraph`, `Importer`, `MutatedProject`, `ImporterToUpdate`, etc.
- Update function signatures in:
  - Core install/mutate functions
  - Plugin commands (rebuild, script runners, installation, patching)
  - Workspace utilities (filter, sort, pkgs-graph)
  - Resolution and context modules
- Add `as ProjectRootDir` type assertions where paths are known to be project roots
- Update test fixtures to use branded types

## Benefits

- **Type safety**: Compile-time checks prevent passing arbitrary strings as project roots
- **Self-documenting**: Clear intent when a path must be a project root directory
- **Maintainability**: Easier to track and refactor path handling logic