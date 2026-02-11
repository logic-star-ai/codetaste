# Summary

This repository contains Kedro, a toolbox for production-ready data science that helps create data engineering and data science pipelines that are reproducible, maintainable, and modular.

## System Dependencies

- **No system-level dependencies required**: All dependencies are Python packages installed through uv/pip
- System services: None required

## Project Environment

- **Language**: Python
- **Python Version**: Python 3.9+ (using Python 3.9.25 for testing)
- **Package Manager**: uv (with pip fallback)
- **Virtual Environment**: Created at `/testbed/.venv`
- **Package Installation**: Editable install with test dependencies (`kedro[test]`)
- **Key Dependencies**:
  - pytest (test framework)
  - pytest-cov (coverage testing)
  - pytest-json-report (test result reporting)
  - behave (BDD testing framework)
  - Various kedro dependencies (click, cookiecutter, dynaconf, etc.)

## Testing Framework

- **Framework**: pytest
- **Test Location**: `/testbed/tests/`
- **Total Tests**: 1,713 tests
- **Test Execution Time**: ~9-11 minutes (without parallelization)
- **Test Configuration**: Defined in `pyproject.toml` under `[tool.pytest.ini_options]`
- **Coverage**: Tests use coverage reporting with strict 100% requirement
- **Parallelization**:
  - The Makefile specifies `--numprocesses 4 --dist loadfile` for parallel execution
  - However, this causes serialization issues with KedroContext objects in some tests
  - Our run_tests script runs tests sequentially to avoid these issues
  - Running sequentially still completes in ~10 minutes, which is within the 15-minute target

## Additional Notes

### Test Results
- **Passed**: 1,658 tests
- **Failed**: 54 tests (related to starter templates and tool configurations)
- **Skipped**: 1 test (lambda function not supported yet)
- **Total**: 1,713 tests

The failed tests appear to be related to template generation and configuration validation, not core functionality issues. These failures are consistent across both HEAD and HEAD~1 commits.

### pytest-xdist Issue
The tests have a known issue with pytest-xdist parallelization where KedroContext objects cannot be serialized across worker processes. This manifests as `execnet.gateway_base.DumpError: can't serialize <class 'kedro.framework.context.context.KedroContext'>`. The solution was to run tests sequentially, which still meets the 15-minute time constraint.

### Script Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications, as required.
