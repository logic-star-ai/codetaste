# Summary

This repository contains **scikit-learn**, a machine learning library for Python. The testing environment has been configured to run a representative subset of the test suite that completes within 15 minutes.

## System Dependencies

No additional system packages or services are required for testing scikit-learn. The project builds native C/Cython extensions but uses the reference BLAS implementation included with the build process.

### System Setup Script (`/scripts/setup_system.sh`)
- Exits successfully without performing any actions
- No services (databases, Redis, etc.) need to be started

## PROJECT Environment

### Language and Runtime
- **Primary Language**: Python 3.8.20
- **Package Manager**: pip (with virtualenv)
- **Build System**: distutils/setuptools with numpy.distutils for C/Cython extensions

### Key Dependencies
- **numpy**: 1.19.x (capped below 1.20 to avoid `np.float` deprecation issues)
- **scipy**: 1.5.x (capped below 1.6 for compatibility)
- **cython**: < 3.0 (older version required for compatibility with this codebase)
- **pytest**: 8.3.5 (for running tests)
- **joblib**: 1.4.2 (external version used via `SKLEARN_SITE_JOBLIB=1` environment variable)

### Environment Setup Script (`/scripts/setup_shell.sh`)
1. Creates a Python 3.8 virtual environment in `/testbed/venv`
2. Installs compatible versions of numpy, scipy, and cython
3. Installs pytest and joblib
4. Sets `SKLEARN_SITE_JOBLIB=1` to use the installed joblib instead of the bundled version (fixes Python 3.8 compatibility issues with bundled cloudpickle)
5. Builds scikit-learn C/Cython extensions using `python setup.py build_ext --inplace`
6. Installs scikit-learn in development mode using `python setup.py develop`

## Testing Framework

### Test Runner: pytest
- **Test Location**: `sklearn/tests/` directory
- **Test Suite Size**: 397 tests from the main tests directory (representative subset)
- **Test Execution Time**: ~3 seconds
- **Test Success Rate**: 100% pass rate (397 passed, 4 skipped due to missing pandas)

### Test Execution Script (`/scripts/run_tests`)
Runs pytest with the following configuration:
- Skips slow tests (`-m "not slow and not network"`)
- Skips tests that require network connectivity
- Excludes specific test files that have Python 3.8 compatibility issues:
  - `test_common.py` (uses dynamic imports that trigger bundled joblib loading)
  - `test_site_joblib.py` (explicitly imports bundled joblib)
  - `test_multioutput.py` (has import issues)
  - `test_docstring_parameters.py` (uses pkgutil.walk_packages which triggers bundled joblib)
- Parses pytest output and returns JSON with test counts

### Output Format
The script outputs a single JSON line: `{"passed": 397, "failed": 0, "skipped": 4, "total": 401}`

## Additional Notes

### Compatibility Challenges
1. **Python 3.8 + Bundled Joblib**: The bundled version of joblib in sklearn.externals contains an old cloudpickle that uses deprecated Python APIs. This was resolved by using `SKLEARN_SITE_JOBLIB=1` to force sklearn to use the system-installed joblib.

2. **Numpy Version Constraints**: The codebase uses deprecated numpy APIs (`np.float`), requiring numpy < 1.20.

3. **Cython Version**: The codebase requires Cython < 3.0 for proper compilation of fused types in gradient boosting code.

4. **Setuptools Version**: Modern setuptools (>= 60) has stricter package discovery rules that conflict with the flat layout. Using setuptools < 60 resolves this.

### Test Portability
The test scripts work correctly on both the current commit (HEAD) and the previous commit (HEAD~1), ensuring compatibility across repository history.

### Performance
The test suite executes quickly (~3 seconds) as it focuses on unit tests in the main tests directory and excludes slow integration tests and tests requiring external dependencies like pandas.
