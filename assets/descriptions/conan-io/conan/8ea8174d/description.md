# Refactor: Move model classes from `conans` to `conan.internal` namespace

## Summary

Move all model classes from `conans.model.*` to `conan.internal.model.*` namespace. Pure internal refactoring to better organize the codebase structure.

## Why

- Consolidate internal model classes under `conan.internal` namespace
- Better separation between public API surface and internal implementation
- Improve code organization and maintainability

## Changes

**Namespace Migration:**
- `conans.model.*` → `conan.internal.model.*`

**Key Classes Moved:**
- ConanFile
- Version, VersionRange
- RecipeReference, PkgReference
- Settings, Options, Profile, Conf
- Requirements, Requirement
- PackageType
- ... (all model classes)

**File Renames:**
- `build_info.py` → `cpp_info.py`
- `graph_lock.py` → `lockfile.py`
- `conans/model/rest_routes.py` → `conans/client/rest/rest_routes.py`

**Import Updates:**
- Updated all ~200+ import statements across the codebase
- Updated `conan/__init__.py` to import from new locations

## Breaking Changes

⚠️ **Risk:** Users relying on undocumented `from conans.model` imports (e.g., in custom commands, scripts) will break. These were never part of the public API.

## Impact

- Tests: ✅ Fixed
- Public API: ✅ Unchanged
- Internal API: ⚠️ All `conans.model` imports must update