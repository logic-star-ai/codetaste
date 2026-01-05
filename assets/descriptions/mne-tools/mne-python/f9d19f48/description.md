Title
-----
Add `_check_option` utility for parameter validation

Summary
-------
Add a new private utility function `_check_option` to standardize parameter validation across the codebase and refactor existing validation code to use it.

Why
---
The pattern of checking parameter values against a list of valid options is repeated inconsistently throughout the codebase:

```python
if method not in ['foo', 'bar', 'baz']:
    raise ValueError("Invalid value for 'method' parameter. Valid options are ...")
```

This leads to:
- Code duplication (~100+ occurrences)
- Inconsistent error messages
- Maintenance overhead

Changes
-------
- Add `_check_option(parameter, value, allowed_values)` in `mne/utils/check.py`
  - Validates `value` against `allowed_values`
  - Raises `ValueError` with friendly, consistent error message
  - Handles singular/plural formatting automatically
- Export from `mne/utils/__init__.py`
- Refactor validation checks across:
  - `mne/baseline.py`, `mne/beamformer/`, `mne/channels/`, `mne/chpi.py`
  - `mne/cov.py`, `mne/datasets/`, `mne/decoding/`, `mne/dipole.py`
  - `mne/epochs.py`, `mne/event.py`, `mne/evoked.py`, `mne/filter.py`
  - `mne/fixes.py`, `mne/forward/`, `mne/io/`, `mne/label.py`
  - `mne/minimum_norm/`, `mne/morph.py`, `mne/preprocessing/`
  - `mne/proj.py`, `mne/report.py`, `mne/simulation/`, `mne/source_estimate.py`
  - `mne/stats/`, `mne/time_frequency/`, `mne/viz/`
- Add tests in `mne/utils/tests/test_check.py`
- Update affected tests to match new error messages

Benefits
--------
- Single source of truth for parameter validation
- Consistent, readable error messages
- Less boilerplate code
- Easier to maintain