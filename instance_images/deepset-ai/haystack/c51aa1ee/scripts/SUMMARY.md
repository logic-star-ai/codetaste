# Summary

This repository contains **Haystack**, an end-to-end NLP framework for building LLM applications. The testing infrastructure has been configured to run unit tests across multiple core components using pytest.

## System Dependencies

No system-level dependencies or services are required for the basic unit tests. The test suite uses in-memory data stores and does not require external services like Elasticsearch, Weaviate, or other document stores.

## Project Environment

- **Language**: Python
- **Python Version**: 3.10.19 (compatible with 3.8, 3.9, 3.10, 3.11)
- **Package Manager**: pip with virtual environment
- **Build System**: hatchling (PEP 517)
- **Installation Method**: Editable install with `pip install -e ".[dev]"`

### Key Dependencies

- Core dependencies: transformers, pandas, scikit-learn, requests, pydantic<2
- Testing: pytest, pytest-cov, pytest-asyncio, pytest-custom-exit-code
- Development: black, mypy, pylint, pre-commit
- Framework: Includes nodes for retrieval, generation, and various NLP tasks

## Testing Framework

- **Framework**: pytest 9.0.2
- **Test Organization**: Tests are organized by component in `test/` directory:
  - `test/agents/` - Agent-related tests
  - `test/cli/` - CLI tool tests
  - `test/utils/` - Utility function tests
  - `test/pipelines/` - Pipeline tests
  - `test/others/` - Miscellaneous tests

### Test Execution

- **Markers**: Tests use pytest markers (`unit`, `integration`, etc.)
- **Configuration**: Tests use `--document_store_type=memory` to avoid external dependencies
- **Scope**: Runs approximately 216 unit tests representing core functionality
- **Performance**: Completes in ~20-30 seconds

### Test Results

- **Passed**: 200 tests
- **Failed**: 16 tests (primarily due to optional dependencies not installed)
- **Total**: 216 tests

The failed tests are expected failures due to:
1. Missing optional dependencies (rapidfuzz for metrics)
2. Import errors for torch-dependent features
3. Deprecated numpy functions in some test files

## Additional Notes

### Excluded Test Files

The following test files are excluded from the test run due to import errors:
- `test/pipelines/test_pipeline_yaml.py` - Uses deprecated numpy.mat
- `test/others/test_squad_data.py` - Requires torch (optional dependency)

### Virtual Environment

The setup script creates a persistent virtual environment in `.venv/` that is reused across runs for efficiency. The `.deps_installed` marker file tracks whether dependencies have been installed to avoid redundant installations.

### Portability

The scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification, as verified during setup. The test suite produces consistent results across both commits.

### Environment Variables

- `HAYSTACK_TELEMETRY_ENABLED=False` - Disables telemetry during tests
- `PYTHONDONTWRITEBYTECODE=1` - Prevents .pyc file creation
