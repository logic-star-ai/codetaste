Title
-----
Reorganize `django.db.backends` classes into separate modules

Summary
-------
Refactor backend database classes from single monolithic files into separate, logically organized modules within `django.db.backends.base.*` and update all backend implementations accordingly.

Why
---
- Current structure has all base classes (`BaseDatabaseWrapper`, `BaseDatabaseFeatures`, `BaseDatabaseOperations`, etc.) crammed into `django/db/backends/__init__.py` (~1500 lines)
- Makes codebase harder to navigate and maintain
- Inconsistent with typical pattern where `DatabaseFoo` classes live in `foo.py`
- Backend-specific files (mysql, oracle, postgresql, sqlite) mix multiple concerns

Changes
-------
**Core backend reorganization:**
- Create `django/db/backends/base/` package
- Split classes into separate modules:
  - `base.py` → `BaseDatabaseWrapper`
  - `features.py` → `BaseDatabaseFeatures`
  - `operations.py` → `BaseDatabaseOperations`
  - `introspection.py` → `BaseDatabaseIntrospection`
  - `client.py` → `BaseDatabaseClient`
  - `validation.py` → `BaseDatabaseValidation`
  - `schema.py` → `BaseDatabaseSchemaEditor`

**Backend implementations (mysql, oracle, postgresql_psycopg2, sqlite3):**
- Split monolithic `base.py` files into separate modules matching base structure
- Extract `DatabaseFeatures` → `features.py`
- Extract `DatabaseOperations` → `operations.py`
- Create utility modules where needed (e.g., `utils.py` for helper functions)
- Update imports throughout

**GIS backends:**
- Apply same pattern to `django.contrib.gis.db.backends.*`
- Move classes to `base/features.py`, `base/operations.py`, `base/models.py`, `base/adapter.py`
- Update all GIS backend imports

**Update imports across codebase:**
- Change `from django.db.backends import BaseDatabaseXXX` → `from django.db.backends.base.XXX import BaseDatabaseXXX`
- Update documentation references
- Fix all test imports

Implementation
--------------
- [ ] Create `django/db/backends/base/` package structure
- [ ] Move and split base classes into separate modules
- [ ] Refactor mysql backend
- [ ] Refactor oracle backend  
- [ ] Refactor postgresql_psycopg2 backend
- [ ] Refactor sqlite3 backend
- [ ] Reorganize GIS backends
- [ ] Update all imports across Django codebase
- [ ] Update documentation
- [ ] Update tests