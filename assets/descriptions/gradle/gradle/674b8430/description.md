# Title

Refactor `ProjectIdentity` to enforce path invariants and remove DM dependencies

# Summary

Cleanup and refactor `ProjectIdentity` to enforce the relationship between build path, project path, and identity path. Replace `BuildIdentifier` with `Path` to remove dependency on DM types, and introduce restricted factory methods to guarantee invariants for root vs. non-root projects.

# Why

- `ProjectIdentity` allowed arbitrary construction without enforcing the invariant that `identityPath = buildPath.append(projectPath)`
- `BuildIdentifier` is a dependency management type that shouldn't be used in build structure/configuration classes
- Since 9.0, `BuildIdentifier` is just a wrapper around `Path`, making it redundant
- Different project types (root vs. subproject, same build vs. different build) required special-case serialization logic

# Changes

## ProjectIdentity
- Replace `BuildIdentifier` parameter with `Path` for build path
- Add factory methods:
  - `ProjectIdentity.forRootProject(Path buildPath, String projectName)` - root project has `Path.ROOT` as project path
  - `ProjectIdentity.forSubproject(Path buildPath, Path projectPath)` - subproject name must match last element of project path
- Enforce invariant: `identityPath = buildPath.append(projectPath)` by construction
- Add static helper: `computeProjectIdentityPath(buildPath, projectPath)`

## Serializers
- Simplify `ComponentIdentifierSerializer` - collapse 4 project cases into 1
- Simplify `ComponentSelectorSerializer` - collapse 4 project cases into 1
- Add `ProjectIdentitySerializer` to handle project identity serialization
- Add `PathSerializer` for efficient `Path` serialization (special-case `Path.ROOT`)
- Simplify `BuildIdentifierSerializer` to delegate to `PathSerializer`

## Build Registry
- Change `BuildStateRegistry` methods from `BuildIdentifier` → `Path`:
  - `getBuild(Path)` / `findBuild(Path)`
- Update internal maps from `Map<BuildIdentifier, ...>` → `Map<Path, ...>`

## Test Updates
- Update all test code to use new factory methods
- Use `ProjectIdentity.forRootProject(...)` for root projects
- Use `ProjectIdentity.forSubproject(...)` for subprojects

# Benefits

- Stronger compile-time guarantees about project identity invariants
- Cleaner separation between DM types and build structure types
- Simpler serialization logic (removed special cases)
- More explicit intent (factory methods vs. raw constructor)