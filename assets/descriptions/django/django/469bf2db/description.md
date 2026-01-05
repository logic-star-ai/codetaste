Title
-----
Simplify imports from `django.db` and `django.contrib.gis.db` modules

Summary
-------
Refactor internal Django codebase to use shorter import paths for commonly used classes/functions that are already exposed at the package level.

Why
---
Many classes were being imported from their deep module paths (e.g., `django.db.models.aggregates.Aggregate`, `django.db.models.fields.CharField`, `django.db.utils.DatabaseError`) when they're already available from shorter paths via `__init__.py` exports.

This creates unnecessary verbosity and inconsistency across the codebase.

Changes
-------
**From `django.db.models.*` submodules → `django.db.models`:**
- Aggregates: `Aggregate`, `Avg`, `Count`, `Max`, `Min`, `StdDev`, `Sum`, `Variance`
- Constraints: `CheckConstraint`, `UniqueConstraint`
- Deletion: `CASCADE`, `DO_NOTHING`, `PROTECT`, `ProtectedError`
- Expressions: `Exists`, `Expression`, `ExpressionWrapper`, `F`, `Func`, `OrderBy`, `Value`
- Fields: `BLANK_CHOICE_DASH`, `NOT_PROVIDED`, `AutoField`, `BooleanField`, `CharField`, `DateTimeField`, `Field`, `IntegerField`, `NullBooleanField`, `OrderWrt`
- Related fields: `ForeignKey`, `ForeignObject`, `ForeignObjectRel`, `ManyToManyField`, `ManyToManyRel`, `OneToOneField`
- Indexes: `Index`
- Lookups: `Lookup`, `Transform`
- Query: `QuerySet`, `Q`

**From `django.db.utils.*` → `django.db`:**
- `DEFAULT_DB_ALIAS`, `DataError`, `DatabaseError`, `IntegrityError`, `NotSupportedError`, `OperationalError`, `ProgrammingError`

**From `django.contrib.gis.db.models.*` submodules → `django.contrib.gis.db.models`:**
- GIS aggregates: `Collect`, `Extent`, `Extent3D`, `MakeLine`, `Union`
- GIS fields: `GeometryCollectionField`, `GeometryField`, `LineStringField`

Scope
-----
- Admin, auth, contenttypes, GIS backends/operations
- Forms, views, migrations, model fields/indexes
- Test suite
- Documentation examples