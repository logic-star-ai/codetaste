# Remove deprecated `annotation` module, `BaseSeriesAnnotator`, `Y` parameter, and `HierarchyEnsembleForecaster.fitted_list`

Execute scheduled deprecations and change actions for 0.37.0 release:
* Remove deprecated `annotation` module → replaced by `detection` module
* Remove `BaseSeriesAnnotator` → replaced by `BaseDetector`
* Remove deprecated `Y` parameter from `BaseDetector` methods → replaced by lowercase `y`
* Remove `HierarchyEnsembleForecaster.fitted_list` property → replaced by `fitted_list_` and `get_fitted_params()`
* Bump all 0.37.0 deprecation/change markers to 0.38.0