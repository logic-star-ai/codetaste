# Test Suite Documentation

Comprehensive test suite for the refactoring-benchmark project.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and test helpers
├── test_bootstrap.py        # Bootstrap phase tests (integration)
├── test_container_utils.py  # Container utility tests (integration)
├── test_logger.py          # Logger tests (unit)
├── test_models.py          # Pydantic model tests (unit)
└── README.md               # This file
```

## Test Categories

### Unit Tests (Fast)
Unit tests have no external dependencies and test individual components in isolation:
- `test_models.py` - Pydantic model validation and serialization
- `test_logger.py` - Logging configuration and output

Run only unit tests:
```bash
pytest -m unit
```

### Integration Tests (Slow)
Integration tests require Docker and test real container operations:
- `test_bootstrap.py` - Full bootstrap workflow with real containers
- `test_container_utils.py` - Docker operations (copy, extract, exec)

Run only integration tests:
```bash
pytest -m integration
```

Skip slow/integration tests:
```bash
pytest -m "not slow"
```

## Key Test Cases

### Critical Tests (Primary Requirements)

#### 1. Repository at Base Commit After Setup Phase
**Test**: `test_repository_at_base_commit_after_setup_phase`
**Location**: `test_bootstrap.py:TestGitCommitVerification`
**Purpose**: Verifies that after `bootstrap_setup_phase()` completes, the repository is checked out at the base/buggy commit (pre-refactoring), NOT the golden commit.

This is the PRIMARY test requirement - it ensures the critical invariant that containers are left in the correct state for agent inference.

**How the mock works**:
- In real bootstrap: `stream_exec()` runs the `claude` CLI command
- The Claude agent (not stream_exec) creates `/scripts/run_tests`, `/scripts/setup_system.sh`, and `/scripts/setup_shell.sh` files
- In tests: We mock `stream_exec` to detect Claude CLI calls and create those scripts directly
- This simulates Claude's output without requiring API calls or credentials

#### 2. Repository at Base Commit After Full Bootstrap
**Test**: `test_repository_at_base_commit_after_full_bootstrap`
**Location**: `test_bootstrap.py:TestGitCommitVerification`
**Purpose**: Verifies that after the complete `bootstrap_instance()` flow (both setup and runtime phases), the repository remains at the base commit.

### Other Important Tests

#### Metrics Capture
- `test_run_test_metrics_success` - Validates JSON test output parsing
- `test_run_test_metrics_failure` - Handles crashed/invalid test output
- `test_success_criteria_validation` - Tests the 10+ tests, 30%+ pass rate criteria

#### Runtime Phase Injections
- `test_entrypoint_injection` - Verifies entrypoint.sh is injected and executable
- `test_rules_injection_with_permissions` - Verifies rules are injected with root:root 700 (hidden from agent)
- `test_task_description_injection_with_permissions` - Verifies descriptions with benchmarker:benchmarker 755 (visible to agent)

#### Container Utilities
- `test_copy_file_to_container` - File copying to containers
- `test_extract_folder` - Folder extraction from containers
- `test_stream_exec_*` - Command execution with streaming output

## Running Tests

### Run All Tests
```bash
poetry run pytest
```

### Run Specific Test File
```bash
poetry run pytest tests/test_models.py
```

### Run Specific Test
```bash
poetry run pytest tests/test_bootstrap.py::TestGitCommitVerification::test_repository_at_base_commit_after_setup_phase
```

### Run Tests with Coverage
```bash
poetry run pytest --cov=refactoring_benchmark --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### Run Tests in Verbose Mode
```bash
poetry run pytest -vv
```

### Run Tests with Output
```bash
poetry run pytest -s
```

## Test Fixtures

### Docker Fixtures
- `docker_client` - Session-scoped Docker client
- `cleanup_test_images` - Cleans up test Docker images after tests

### Data Fixtures
- `sample_instance_row` - Example InstanceRow for testing
- `sample_metrics` - Example Metrics object
- `temp_dir` - Temporary directory, auto-cleaned

### Helper Functions (conftest.py)
- `get_git_commit_hash(container, cwd)` - Get current commit in container
- `verify_git_state(container, expected_hash, cwd)` - Verify commit matches expected
- `container_file_exists(container, path)` - Check if file exists
- `container_dir_exists(container, path)` - Check if directory exists
- `get_file_permissions(container, path)` - Get file permissions (e.g., "755")
- `get_file_owner(container, path)` - Get file owner and group

## Prerequisites

### For All Tests
```bash
poetry install --with dev
```

### For Integration Tests
1. Docker or Podman must be running:
   ```bash
   docker ps
   ```

2. Base image must exist:
   ```bash
   cd refactoring_benchmark/base_images/
   docker build -t benchmark-base-python -f Dockerfile.python .
   ```

3. For Podman users:
   ```bash
   export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
   ```

## Test Design Principles

### Minimal Mocking
Tests use real Docker containers when possible to catch real-world issues. Mocking is limited to:
- Claude agent execution (mocked with scripts that create valid test output)
- External API calls (if any)
- Time-consuming operations that don't affect core logic

### Clean and Maintainable
- Clear test names that describe what is being tested
- Docstrings explaining the purpose and expected behavior
- Proper cleanup with try/finally blocks for containers
- Fixtures for common setup/teardown
- Helper functions in conftest.py for repeated operations

### Test Isolation
- Each test is independent
- Temporary directories are created and cleaned up
- Docker containers are stopped and removed after use
- Test images are cleaned up via `cleanup_test_images` fixture

## Continuous Integration

Tests are designed to work in CI environments. For CI pipelines:

```bash
# Skip slow integration tests if Docker is not available
pytest -m "not integration"

# Run with parallel execution (if pytest-xdist is installed)
pytest -n auto

# Generate JUnit XML for CI reporting
pytest --junitxml=test-results.xml
```

## Troubleshooting

### Docker Connection Issues
```bash
# Check Docker is running
docker ps

# Set DOCKER_HOST for Podman
export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock
```

### Base Image Not Found
```bash
cd refactoring_benchmark/base_images/
docker build -t benchmark-base-python -f Dockerfile.python .
```

### Permission Errors
Some tests verify file permissions. If running in rootless Docker/Podman, permission checks may behave differently.

### Slow Tests
Integration tests can be slow. Skip them during development:
```bash
pytest -m "not slow"
```

## Adding New Tests

### For New Features
1. Add test file: `tests/test_feature.py`
2. Import fixtures from `conftest.py`
3. Mark appropriately: `@pytest.mark.unit` or `@pytest.mark.slow`
4. Use descriptive test names: `test_feature_does_what_when_condition`
5. Add docstrings explaining what is being tested

### For Bug Fixes
1. Write a test that reproduces the bug (should fail)
2. Fix the bug
3. Verify test passes
4. Keep the test to prevent regression

## Coverage Goals

Aim for:
- 100% coverage of models and utilities
- 80%+ coverage of bootstrap logic (some error paths are hard to test)
- All critical paths tested (git state, metrics, injections)

Check current coverage:
```bash
pytest --cov=refactoring_benchmark --cov-report=term-missing
```
