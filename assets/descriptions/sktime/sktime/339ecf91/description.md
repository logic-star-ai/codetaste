# Title
-----
Remove deprecated `annotation` module, `BaseSeriesAnnotator`, `Y` parameter, and `HierarchyEnsembleForecaster.fitted_list`

# Summary
-------
Execute scheduled deprecations and change actions for 0.37.0 release:
* Remove deprecated `annotation` module → replaced by `detection` module
* Remove `BaseSeriesAnnotator` → replaced by `BaseDetector`
* Remove deprecated `Y` parameter from `BaseDetector` methods → replaced by lowercase `y`
* Remove `HierarchyEnsembleForecaster.fitted_list` property → replaced by `fitted_list_` and `get_fitted_params()`
* Bump all 0.37.0 deprecation/change markers to 0.38.0

# Changes Required
-----------------

### Remove `annotation` module
- Delete entire `sktime/annotation/` directory and all subdirectories
- Update all imports from `sktime.annotation.*` to `sktime.detection.*` across:
  - Documentation (`docs/source/get_started.rst`)
  - Examples (`examples/annotation/...`)
  - Test files

### Remove `BaseSeriesAnnotator`
- Delete `BaseSeriesAnnotator` class from `sktime.detection.base._base`
- Remove from `__all__` exports in `sktime/detection/base/__init__.py`

### Remove `Y` parameter handling
- Remove `Y` parameter from `BaseDetector.fit()`, `.update()`, `.fit_predict()`, `.fit_transform()`
- Remove deprecation warnings for `Y` parameter
- Remove internal `_fit()` and `_update()` handling for uppercase `Y`

### Remove `fitted_list` property
- Delete `fitted_list` property from `HierarchyEnsembleForecaster`
- Update all references to use `fitted_list_` attribute instead
- Update tests in `test_hierarchy_ensemble.py`

### Bump deprecation markers
- Update all `TODO 0.37.0` comments to `TODO 0.38.0` across:
  - `_probability_threshold.py`
  - `_fh.py`
  - `_pmdarima.py`
  - `test_fh.py`
  - `_pipeline.py`
  - `_tune.py`
  - `timesfm_forecaster.py`
  - `test_lookup.py`

# Context
--------
This is a scheduled maintenance task for version 0.37.0 to remove previously deprecated functionality and clean up backwards compatibility code.