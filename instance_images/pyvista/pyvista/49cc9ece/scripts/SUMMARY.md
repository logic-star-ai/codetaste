# Summary

This repository contains PyVista, a Python library for 3D plotting and mesh analysis powered by VTK (Visualization Toolkit). The testing setup includes Python-based unit tests using pytest, with a focus on core functionality tests that avoid resource-intensive plotting tests and external data downloads.

## System Dependencies

- **Operating System**: Linux (Ubuntu 24.04)
- **Python Version**: 3.11.14 (from pre-installed uv Python installations)
- **Key System Libraries**:
  - OpenGL/Mesa libraries (pre-installed for VTK rendering)
  - Standard build tools and libraries

No additional system packages need to be installed. The system already has the necessary libraries for VTK's offscreen rendering capabilities.

## Project Environment

### Python Dependencies

- **Core Requirements** (from requirements.txt):
  - matplotlib<3.7.2
  - numpy<1.25.0
  - pillow<9.6.0
  - pooch<1.8.0
  - scooby>=0.5.1,<0.8.0

- **VTK Version**: 9.2.6 (pinned for compatibility with Python 3.11)
  - VTK is not listed in requirements.txt by design to allow custom VTK variants
  - Version 9.2.6 is the latest compatible version for Python 3.11 that works with the current PyVista code

- **Test Dependencies** (from requirements_test.txt):
  - pytest<7.4.0
  - pytest-cov, pytest-memprof, pytest-xdist
  - pytest_pyvista==0.1.8
  - Various optional packages (cmocean, colorcet, hypothesis, imageio, meshio, etc.)

### Environment Variables

- `PYVISTA_OFF_SCREEN=True`: Enables headless rendering mode
- `MPLBACKEND=Agg`: Sets matplotlib to non-interactive backend
- `PYTHON_BIN`: Points to Python 3.11 executable

### Installation Method

1. Create Python 3.11 virtual environment
2. Install test dependencies from requirements_test.txt
3. Install VTK 9.2.6 explicitly
4. Install PyVista in editable mode with --no-deps to prevent VTK version conflicts

## Testing Framework

### Framework: pytest

- **Version**: pytest<7.4.0
- **Key Plugins**:
  - pytest-cov: Code coverage
  - pytest-memprof: Memory profiling
  - pytest-xdist: Parallel test execution
  - pytest_pyvista: PyVista-specific test utilities

### Test Execution Strategy

The test suite runs a representative subset of core functionality tests:

- **Included Test Files** (15 files):
  - test_helpers.py
  - test_datasetattributes.py
  - test_dataset.py
  - test_filters.py
  - test_grid.py
  - test_composite.py
  - test_colors.py
  - test_utilities.py
  - test_geometric_objects.py
  - test_pointset.py
  - test_polydata.py
  - test_camera.py
  - test_cells.py
  - test_dataobject.py
  - test_init.py

- **Excluded Tests**:
  - tests/plotting/ (can be resource-intensive and flaky)
  - tests/examples/ (may require external resources)
  - tests/jupyter/ (notebook-specific tests)
  - Tests requiring downloads (filtered via `-k "not download and not test_download"`)

### Test Results

- **Total Tests**: ~1122 tests
- **Typical Execution Time**: 30-50 seconds
- **Expected Results**: 1104 passed, 18 skipped, 2 xfailed, 2 warnings

### JSON Output Format

The run_tests script outputs results in JSON format:
```json
{"passed": 1104, "failed": 0, "skipped": 18, "total": 1122}
```

## Additional Notes

### Challenges Encountered

1. **VTK Version Compatibility**: Initial attempts to use VTK 9.2.2 failed because it's not available for Python 3.11. The solution was to use VTK 9.2.6, which is the latest 9.2.x version compatible with Python 3.11.

2. **VTK Version Pinning**: PyVista's pyproject.toml specifies `vtk` without version constraints to support custom VTK variants (e.g., vtk_osmesa). This caused pip to upgrade VTK during installation. The solution was to install PyVista with `--no-deps` after manually installing the correct VTK version.

3. **Test Segfaults**: Running all tests at once caused segmentation faults, likely due to memory issues or VTK internal state. The solution was to run a curated subset of stable core tests that exercise the main functionality without triggering crashes.

### Script Portability

All three scripts (/scripts/setup_system.sh, /scripts/setup_shell.sh, /scripts/run_tests) are designed to work on both HEAD and HEAD~1 commits without modification. They detect and install dependencies based on the checked-out code.

### Performance Considerations

- Virtual environment is cached in /testbed/.venv for faster subsequent runs
- The setup_shell.sh script is idempotent and checks if packages are already installed
- Tests run sequentially to avoid parallel execution issues
- Memory profiling is enabled to track resource usage
