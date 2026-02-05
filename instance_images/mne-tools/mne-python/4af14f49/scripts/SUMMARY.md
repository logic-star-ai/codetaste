# Summary

This repository contains MNE-Python, a Python package for analyzing MEG, EEG, and other neurophysiological data. The testing setup has been configured to run a representative subset of the test suite in a headless environment.

## System Dependencies

The following system packages are required and installed via `/scripts/setup_system.sh`:

- **Qt/PyQt6 libraries**: Required for pytest-qt and GUI-related tests in headless mode
  - libegl1, libgl1
  - libxkbcommon-x11-0
  - libxcb-* packages (icccm4, image0, keysyms1, randr0, render-util0, shape0, xinerama0, xfixes0, cursor0)
  - libdbus-1-3
  - xvfb (X Virtual Framebuffer)

All system dependencies are installed during the `setup_system.sh` execution.

## PROJECT Environment

### Python Version
- **Python 3.11.14** is used (via uv python manager)
- MNE-Python requires Python >= 3.8

### Virtual Environment
- Location: `/tmp/mne_venv`
- Managed by Python's built-in `venv` module

### Python Dependencies
Key dependencies installed:
- **numpy** >= 1.21.2, < 2.0
- **scipy** >= 1.7.1, < 1.14 (capped to avoid compatibility issues with removed sph_harm)
- **matplotlib** >= 3.4.3
- **pytest** < 9.0 (capped to avoid fixture decorator warnings)
- **pytest-cov, pytest-timeout, pytest-harvest, pytest-qt**
- **pytest-json-report** (for JSON test output)
- **PyQt6** (Qt bindings for GUI tests)
- **scikit-learn, nibabel, pandas, numba, joblib** (additional scientific computing packages)
- **h5io, pymatreader** (HDF5 support)
- Various testing and linting tools (ruff, numpydoc, codespell, black, etc.)

### Environment Variables
The following environment variables are set to ensure proper headless testing:
- `MNE_SKIP_NETWORK_TESTS=1` - Skip tests requiring network
- `MNE_DATASETS_TESTING_PATH=/tmp/mne_testing_data` - Data path for testing
- `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1` - Single-threaded BLAS
- `MNE_3D_BACKEND=pyvista` - 3D visualization backend
- `PYVISTA_OFF_SCREEN=true` - Headless PyVista rendering
- `MPLBACKEND=Agg` - Non-interactive matplotlib backend
- `QT_QPA_PLATFORM=offscreen` - Headless Qt platform
- `DISPLAY=""` - No X display

## Testing Framework

### Test Runner
- **pytest** version 8.4.2
- Uses **pytest-json-report** plugin for JSON output

### Test Subset
The test suite runs a representative subset of core functionality tests covering:
- Annotations and events
- BEM and forward modeling
- Covariance estimation
- Dipole fitting
- Epochs and evoked responses
- Filtering
- Source estimation
- FIFF file I/O and metadata
- Channel handling and layouts
- Raw data I/O
- Preprocessing and artifact detection
- Statistics
- Time-frequency analysis
- Utility functions

### Test Execution
Total tests in subset: ~665 tests
- Tests are run with a 120-second timeout per test
- Slow tests marked as `ultraslowtest` or `pgtest` are excluded
- Test output is captured in JSON format

### Output Format
The `/scripts/run_tests` script outputs a single JSON line to stdout:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Version Compatibility Issues Resolved

1. **scipy >= 1.14 incompatibility**: Recent scipy versions removed `scipy.special.sph_harm`, causing import errors. The setup caps scipy to < 1.14 to maintain compatibility.

2. **pytest 9.0 incompatibility**: pytest 9.0 introduced stricter handling of marks applied to fixtures, causing warnings. The setup caps pytest to < 9.0 to avoid these issues.

3. **Qt/PyQt6 system dependencies**: pytest-qt requires Qt system libraries even in headless mode. The setup_system.sh script installs all necessary EGL and XCB libraries.

### Idempotency
The `/scripts/setup_shell.sh` script is idempotent and uses a marker file (`/tmp/mne_venv/.deps_installed`) to avoid redundant package installations on subsequent runs.

### Portability
All scripts work correctly on both HEAD and HEAD~1 commits without modification, as required by the specifications.

### Test Results
On the current commit (b33f3a8), the representative test subset produces:
- Passed: 531 tests
- Failed: 11 tests
- Skipped: 123 tests
- Total: 665 tests

Some test failures are expected in a minimal testing environment without full datasets downloaded. The key functionality tests pass successfully.
