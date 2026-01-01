# Rename `odb` to `cache` throughout codebase

## Summary
Rename `repo.odb` → `repo.cache` throughout the codebase to clarify terminology and better distinguish between three types of object databases: generic odb (e.g., in-memory), cache (typically local), and remote (typically cloud).

## Why
- Historical naming inconsistency - was called `cache` before
- Need clearer distinction between odb types
- Preparation for introducing `out.odb` and `out.cache` attributes
- Aligns with upcoming dvc-data migration

## Changes
- `dvc/odbmgr.py` → `dvc/cachemgr.py`
- `ODBManager` class → `CacheManager` class  
- All `repo.odb` references → `repo.cache`
- All `dvc.odb` references → `dvc.cache`
- Update imports: `from dvc.odbmgr import ODBManager` → `from dvc.cachemgr import CacheManager`

## Scope
- Core repo initialization & configuration
- Data cloud push/pull/fetch operations
- Output building & checkout
- Dependencies & external repos
- Stage caching
- GC, diff, import/export flows
- Tests & test fixtures