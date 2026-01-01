# Decouple core and plotting APIs to improve imports and tighten public namespace

## Summary
Refactor PyVista's internal structure to separate `pyvista.core` (data structures, filters) from `pyvista.plotting` (visualization, rendering) to improve modularity, eliminate circular imports, and enable graphics-independent usage of core API.

## Why
- Circular import issues preventing proper code organization
- Core data structures unnecessarily coupled to libGL-dependent VTK modules
- `pyvista.utilities` module had massive scope creep with unclear responsibilities
- Unable to run import checks (flake8, isort) on `__init__.py` files due to circular dependencies
- Public namespace cluttered with unintentional exports

## Changes

### VTK Module Split
- Split `pyvista._vtk` → `pyvista.core._vtk_core` (GL-independent) + `pyvista.plotting._vtk` (GL-dependent)
- Provides clear demarcation between rendering and non-rendering VTK imports

### Move Texture to Plotting
- `pyvista.core.Texture` → `pyvista.plotting.Texture` (requires `vtkTexture` from rendering modules)
- Still accessible via `pyvista.Texture` for backward compatibility

### Deprecate and Reorganize Utilities
- **Deprecated**: `pyvista.utilities` module
- **Split into**:
  - `pyvista.core.utilities.*` (arrays, cells, fileio, geometric_objects, helpers, points, transformations, etc.)
  - `pyvista.plotting.utilities.*` (plotting-specific helpers)
- Implemented `__getattr__` fallback for backward compatibility
- Broke up monolithic `helpers` module into focused submodules

### Rename Internal Module
- `pyvista.plotting.plotting` → `pyvista.plotting.plotter` (module was overriding package namespace)

### Extract `plot()` Function
- Created `pyvista._plot.py` containing the `plot()` helper
- Allows binding to datatypes before importing plotting module
- Enables future full decoupling where plotting is optional

### Import Cleanup
- Eliminated star imports (except intentional cases)
- Consistent import convention: relative for same-level/below, absolute for outside/above
- **Enabled flake8/isort checks on all `__init__.py` files** (previously excluded)
- Fixed numerous incorrect import paths throughout tests, docs, examples

### Type Hints Organization
- Created `pyvista.core._typing_core` for core type aliases
- Separated from plotting-specific types in `pyvista.plotting._typing`

## Impact
- ✅ Public `pyvista.*` namespace unchanged (verified via namespace tests)
- ✅ No breaking changes to main API
- ✅ Internal imports now properly structured
- ✅ Foundation for making plotting truly optional in future work
- ✅ Easier contribution workflow (clear separation of concerns)

## Testing
- Added `tests/namespace/` with pre-refactor baseline
- All existing tests pass with updated import paths
- Integration tests ignore deprecation warnings

---

**Related**: Closes #3764, addresses #4445