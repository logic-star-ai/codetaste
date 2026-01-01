Title
-----
Move unit types to separate package and rename `UnitType` to `Type`

Summary
-------
Refactor repository unit types by moving them from `models/unit.go` to dedicated package `models/unit/` and renaming `UnitType` to `Type` for consistency.

Why
---
- Better package organization and separation of concerns
- Cleaner namespace: `unit.Type` instead of `models.UnitType`
- Reduces clutter in root models package
- Follows Go package structuring best practices

Changes
-------
**Package Structure:**
- Created new package `models/unit`
- Moved `models/unit.go` → `models/unit/unit.go`
- Type rename: `UnitType` → `Type`

**Updated References:**
- All `models.UnitType*` → `unit.Type*` or `unit_model.Type*`
- All `models.Units` → `unit.Units`
- Function `loadUnitConfig()` → `LoadUnitConfig()` (exported)
- Constants: `UnitTypeCode`, `UnitTypeIssues`, ... → `TypeCode`, `TypeIssues`, ...
- Variables: `AllRepoUnitTypes`, `DefaultRepoUnits`, ... → `unit.AllRepoUnitTypes`, ...

**Import Updates:**
- Added `unit_model "code.gitea.io/gitea/models/unit"` or `"code.gitea.io/gitea/models/unit"` throughout codebase
- Updated ~50+ files with new import paths

**Affected Areas:**
- API routes & handlers
- Repository permissions
- Team/org management  
- Issue/PR handling
- Wiki functionality
- LFS server
- Notifications
- Web routes