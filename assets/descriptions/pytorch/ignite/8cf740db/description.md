# Refactor: Move contrib metrics to core metrics module

## Summary
Migrate all metrics from `ignite.contrib.metrics` to `ignite.metrics`, including regression metrics submodule. Update imports, tests, and documentation accordingly.

## Details

**Files to Move:**
- `average_precision.py`
- `cohen_kappa.py`
- `gpu_info.py`
- `precision_recall_curve.py`
- `roc_auc.py`
- `regression/*.py` (all regression metrics)

**Migration Pattern:**
1. Move implementation files from `ignite/contrib/metrics/` → `ignite/metrics/`
2. Replace old files w/ deprecation stubs importing from new location
3. Add deprecation warnings (v0.5.1, removal in v0.6.0)
4. Update `__init__.py` files to expose metrics at top level
5. Migrate tests from `tests/ignite/contrib/metrics/` → `tests/ignite/metrics/`
6. Update all imports across codebase (examples, engines, etc.)

**Documentation Updates:**
- Update `docs/source/metrics.rst` to include all metrics
- Mark `docs/source/contrib/metrics.rst` as deprecated
- Update README.md references
- Fix `defaults.rst` import examples

**Test Updates:**
- Rename test modules for clarity
- Add deprecation warning tests in `test_warnings_of_deprecation_of_metrics.py`
- Adjust test precision where needed (e.g., `test_mean_error.py` intermittent failures)

**Additional Changes:**
- Update `ignite.contrib.engines.common` to import `GpuInfo` from core
- Fix version references in `ignite/engine/__init__.py`
- Consolidate regression metrics under `ignite.metrics.regression` module

## Why
- Promote widely-used metrics to core module
- Improve discoverability
- Align with library evolution
- Maintain backward compatibility via deprecation warnings